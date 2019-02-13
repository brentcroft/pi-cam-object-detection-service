"""


"""
from os.path import join
from os.path import exists
from copy import deepcopy
from platform import node
import traceback

import math
import tensorflow
"""


"""
from cam_config import check_service
from cam_config import read_config
from cam_config import get_config_text
from cam_config import maybe_cache_graph

from detection import init_graph
from detection import build_tensor
from detection import detect_forever

from boxes import box_area
from boxes import box_centre_move
from boxes import get_box_centre
from boxes import distance
from boxes import get_min_max

from util import log_message
from util import timestamp

from storage import store_image_and_detection_files
from storage import store_boxed_image

from still_camera import StillCamera
"""

    global config subsequently updated frequently

"""
config = read_config( log = True )

graph_path, labels_path = maybe_cache_graph( config=config )

detection_graph, label_map, categories, category_index = init_graph( 
    graph_path=graph_path, 
    labels_path=labels_path, 
    num_classes=config['GRAPH_NUM_CLASSES'] 
)

camera = StillCamera( 
    resolution = config['CAMERA_RESOLUTION'], 
    rotation = config['CAMERA_ROTATION'] 
)
"""

    Return a string that can be used as an image filename.
    
    By default, this has a date-time prefix followed by the node id, 
    to ensure reasonable uniqueness, 
    and so that files from multiple nodes sort in calendar order.

"""
def new_image_uri( node_id = None ):
    return "{}-{}".format( 
        timestamp(), 
        node_id 
    )
"""

    Called during detection when an object is detected in an image.
    
    The key filter is on score thresholds.
    
"""    
def detection_filter( class_name=None, score=None, box=None, frame=None ):

    # default is None
    class_min_scores = config['DETECTION_CLASS_MIN_SCORE'] if 'DETECTION_CLASS_MIN_SCORE' in config else None
    
    # default is None
    default_min_score = config['DETECTION_MIN_SCORE'] if 'DETECTION_MIN_SCORE' in config else None
        
    # only one min is applied
    if class_min_scores is not None and class_name in class_min_scores:
        if score < class_min_scores[ class_name ]:
            return False
    elif default_min_score is not None and score < default_min_score:
        return False

    # default is False
    log_rejections = 'LOG_REJECTIONS' in config and config['LOG_REJECTIONS']
    
    #
    w, h = (  box[2] - box[0], box[3] - box[1] )
        
    # 
    if 'BOX_AREA_MIN_MAX_RATIO' in config:
        min_ratio, max_ratio = config['BOX_AREA_MIN_MAX_RATIO']
        root_area_ratio = math.sqrt( float( box_area( box ) ) / float( box_area( frame ) ) )
        
        if root_area_ratio > max_ratio:
            # default is False
            if log_rejections:
                log_message( "BOX_AREA_MIN_MAX_RATIO [{}] rejected-max: root_area_ratio={}".format( max_ratio, root_area_ratio ) )
            return False
            
        if root_area_ratio < min_ratio:
            if log_rejections:
                log_message( "BOX_AREA_MIN_MAX_RATIO [{}] rejected-min: root_area_ratio={}".format( min_ratio, root_area_ratio ) )
            return False

    
    if 'BOX_DIM_MAX_RATIO' in config:
        max_width_ratio, max_height_ratio = config['BOX_DIM_MAX_RATIO']
        fw, fh = (  frame[2] - frame[0], frame[3] - frame[1] )
        width_ratio, height_ratio = ( float( w ) /  fw ), ( float( h ) /  fh )

        if width_ratio > max_width_ratio:
            if log_rejections:
                log_message( "BOX_DIM_MAX_RATIO [{}] rejected: width-ratio ({}/{})={}".format( max_width_ratio, w, fw , width_ratio) )
            return False
            
        if height_ratio > max_height_ratio:
            if log_rejections:
                log_message( "BOX_DIM_MAX_RATIO [{}] rejected: height-ratio ({}/{})={}".format( max_height_ratio, h, fh, height_ratio ) )
            return False    

    if 'BOX_DIM_MAX_DEVIATION' in config:
        max_box_deviation = config['BOX_DIM_MAX_DEVIATION']
        box_deviation = abs( float( max( w, h ) ) / min( w, h ) )
       
        if box_deviation > max_box_deviation:
            if log_rejections:
                log_message( "BOX_DIM_MAX_DEVIATION [{}] rejected: deviation={}".format( max_box_deviation, box_deviation ) )
            return False
            
    return True 
"""

    Called during detection.
    
    Maybe adjust the centre of the frame towards the centre of the target.
    
"""
def maybe_move( frame=None, target=None, step=0, max_size=None ):

    frame_centre = get_box_centre( frame )
    origin_centre = get_box_centre( target )
    
    dist = distance( origin_centre, frame_centre )
    
    if dist > step:
        box_centre_move( box=frame, centre=origin_centre, step=step, max_size=max_size ) 
        #log_message( "  moving: dist=[{:.2f}/{}], from={}, to={}".format( dist, step, frame_centre, origin_centre ) )
"""

    Called during detection when no objects are detected in an image.
    
    1. untrack boxes (return to origin)
    
"""    
def on_no_objects( context = None ):

    # might create an empty boxed image in CURRENT_IMAGE_STORE
    store_boxed_image( context = context, config = config )            

    # default is True
    box_tracker = 'BOX_TRACKER' not in config or config['BOX_TRACKER']
    
    # maybe move frame back towards origin
    if box_tracker:
        box_tracker_return_ratio = config['BOX_TRACKER_RATIOS'][-1] if 'BOX_TRACKER_RATIOS' in config else 8
    
        raw_image = context['raw'][0]
        maybe_move( 
            frame=config['CURRENT_FRAME'], 
            target=config['DETECTION_FRAME'], 
            step=box_tracker_return_ratio,
            max_size=raw_image.size
        )
"""

    called during detection when objects are detected in an image
    1. store data as required
    2. track boxes

"""    
def on_detected_objects( context = None ):

    seq, stats = context['seq'], context['stats']
    
    # default is True
    log_detections = 'LOG_DETECTIONS' not in config or config['LOG_DETECTIONS']
    
    if log_detections and stats is not None:
        num_objects, duration, s_per_i, i_per_s = stats
        log_message( 'Detections: total=[{:>3}], seq={:>3}; {}s [{} s/i, {} i/s].'.format( num_objects, seq, duration, s_per_i, i_per_s ) )                       

    # maybe store images and detections
    stored_paths = store_image_and_detection_files( context=context, config=config )

    # maybe store boxed images
    store_boxed_image( context=context, config=config, stored_paths=stored_paths )                    

    # maybe move frame towards centre of boxes
    # default is True
    box_tracker = 'BOX_TRACKER' not in config or config['BOX_TRACKER']
    
    if box_tracker:

        # default is 6
        box_tracker_track_ratio = config['BOX_TRACKER_RATIOS'][0] if 'BOX_TRACKER_RATIOS' in config else 6
        
        raw_image, raw_meta_data = context['raw']
        
        objects =  raw_meta_data['objects']
        boxes = [ object['box'] for object in objects ]
        
        maybe_move( 
            frame       = config['CURRENT_FRAME'], 
            target      = get_min_max( boxes=boxes, source_scale=( raw_image.width, raw_image.height ) ), 
            step        = box_tracker_track_ratio, 
            max_size    = raw_image.size 
        )        
"""
    
    run

"""
try:
    config['CURRENT_FRAME'] = deepcopy( config['DETECTION_FRAME'] )
    
    camera.start()

    with detection_graph.as_default():
        with tensorflow.Session() as session:
        
            def next_image(): 
            
                # raises exception if suspended
                # otherwise returns service properties
                service = check_service()
                
                # default is platform.node()
                service_node_id = service['NODE_ID'] if 'NODE_ID' in service else node()

                # reload config
                if 'NO_RELOAD' not in config or not config['NO_RELOAD']:
                    current_frame = config['CURRENT_FRAME']
                    config.clear()
                    config.update( read_config() )
                    config['CURRENT_FRAME'] = current_frame
                
                # default is True
                box_tracker = 'BOX_TRACKER' not in config or config['BOX_TRACKER']
                
                # always reset CURRENT_FRAME if not tracking
                if not box_tracker:
                    config['CURRENT_FRAME'] = deepcopy( config['DETECTION_FRAME'] )

                image = camera.pil_image()
                image_uri = new_image_uri( node_id = service_node_id )

                # create new context
                return { 
                    'uri': image_uri, 
                    'raw': ( image, None ) 
                }

            tensor = build_tensor( category_index )
        
            detect_forever( 
                next_image = next_image, 
                on_no_objects = on_no_objects, 
                on_detected_objects = on_detected_objects, 
                config = config, 
                session = session, 
                tensor = tensor,
                constraint = detection_filter
            )

# don't want to return errors to calling script            
except Exception as e:
    message = "{}".format( e )
    
    log_message( "{}".format( e ) )
    
    ok_messages = [
        "Hit max. seq",
        "Service was suspended"
    ]
    
    oks = [ ok for ok in ok_messages if message.startswith( ok ) ]
    
    if len( oks ) == 0:        
        log_message( traceback.format_exc() )

finally:
    camera.stop()
    
