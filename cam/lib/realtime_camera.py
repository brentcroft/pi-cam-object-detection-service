"""


"""
from os.path import join
from os.path import exists
from copy import deepcopy
from platform import node

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
from detection import detect

from boxes import box_area
from boxes import boxes_move
from boxes import box_centre_move
from boxes import get_box_centre
from boxes import distance
from boxes import get_min_max

from util import log_message
from util import timestamp

from ground_truth import put_file_meta
from storage import store_image_and_detection_files
from storage import store_boxed_image

from still_camera import StillCamera
"""
    Called during detection when an object is detected in an image.
    
    Returns False if:
    
    1. the object class name is specified in CLASS_MIN_SCORE 
       and the object score is less than specified
    
    2. the object class score is NOT specified in CLASS_MIN_SCORE 
       and the object score is less than MIN_SCORE
    
    3. the square root of the ratio of the object box area to detection frame area is 
       either greater than MAX_BOX_RATIO or less than MIN_BOX_RATIO
    
    4. reject if the ratio of the object box's width to height, or the inverse, is greater than MAX_BOX_DEVIATION
"""    
def detection_filter( class_name=None, score=None, box=None, frame=None ):
    
    default_min_score, class_min_scores, max_box_ratio, min_box_ratio, max_box_deviation = ( 
        config['MIN_SCORE'], config['CLASS_MIN_SCORE'], 
        config['MAX_BOX_RATIO'], config['MIN_BOX_RATIO'], config['MAX_BOX_DEVIATION']
    )

    # only one min is applied
    if class_min_scores is not None and class_name in class_min_scores and score < class_min_scores[ class_name ]:
        return False
    elif score < default_min_score:
        return False

    # 
    root_area_ratio = math.sqrt( float( box_area( box ) ) / float( box_area( frame ) ) )
    
    if root_area_ratio > max_box_ratio:
        return False
        
    if root_area_ratio < min_box_ratio:
        return False

    #
    w, h = (  box[2] - box[0], box[3] - box[1] )
    ar = abs( float( max( w, h ) ) / min( w, h ) )
    
    if ar > max_box_deviation:
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
        log_message( "  moving: dist=[{:.2f}/{}], from={}, to={}".format( dist, step, frame_centre, origin_centre ) )
"""
    Called during detection when no objects are detected in an image.
    
    1. untrack boxes (return to origin)
"""    
def on_no_objects( image_uri, raw_image, frame_image ):

    # might create an empty boxed image in CURRENT_IMAGE_STORE
    store_boxed_image( 
        image = frame_image if config['STORAGE'] == 1 else raw_image, 
        config = config 
    )            

    # maybe move frame back towards origin
    if config['BOX_TRACKER']:
        maybe_move( 
            frame=config['CURRENT_FRAME'], 
            target=config['DETECTION_FRAME'], 
            step=config['BOX_TRACKER_RATIOS'][-1],
            max_size=raw_image.size
        )
"""
    called during detection when objects are detected in an image
    1. store data as required
    2. track boxes
"""    
def on_detected_objects( seq, image_uri, raw_image, frame_image, meta_data, stats ):

    if stats is not None:
        num_objects, duration, s_per_i, i_per_s = stats
        log_message( 'Detections: total={}, seq={}; {}s [{} s/i, {} i/s].'.format( num_objects, seq, duration, s_per_i, i_per_s ) )                       
    
    objects =  meta_data['objects']
    boxes = [ object['box'] for object in objects ]
    
    # calculate now in case boxes move
    min_max_coords = get_min_max( 
        boxes = boxes, 
        source_scale=( raw_image.width, raw_image.height ) 
    )
    
    
    if config['STORAGE'] == 1:
        boxes_move( 
            boxes = boxes, 
            displacement = config['CURRENT_FRAME'], 
            subtract = True 
        )
        image = frame_image
    else:
        image = raw_image
    
    meta_data['size'] = ( image.width, image.height, 3 )

    stored_paths = store_image_and_detection_files( 
        image_uri=image_uri, 
        image=image, 
        meta_data=meta_data, 
        config=config
    )

    store_boxed_image( 
        image = image, 
        meta_data = meta_data, 
        stored_paths = stored_paths, 
        config=config 
    )                    

    # maybe move frame towards centre of boxes
    if config['BOX_TRACKER']:
        maybe_move( 
            frame=config['CURRENT_FRAME'], 
            target=min_max_coords, 
            step=config['BOX_TRACKER_RATIOS'][0],
            max_size=raw_image.size
        )        
"""


"""
config = read_config( log = True)

config['CURRENT_FRAME'] = deepcopy( config['DETECTION_FRAME'] )


graph_path, labels_path = maybe_cache_graph( config = config )

detection_graph, label_map, categories, category_index = init_graph( 
    graph_path=graph_path, 
    labels_path=labels_path, 
    num_classes=config['NUM_CLASSES'] 
)

camera = StillCamera( 
    image_path = join( config['CURRENT_IMAGE_STORE'], "{}.jpg".format( config['CURRENT_IMAGE_NAME'] ) ),
    resolution = config['CAM_IMAGE_RESOLUTION'], 
    rotation = config['CAM_IMAGE_ROTATION'] 
)

try:
    camera.start()

    with detection_graph.as_default():
        with tensorflow.Session() as session:
        
            def next_image(): 
                check_service()
                config.update( read_config() )
                
                if not config['BOX_TRACKER']:
                    config['CURRENT_FRAME'] = deepcopy( config['DETECTION_FRAME'] )

                return [ "{}-{}".format( timestamp(), node() ),  camera.pil_image() ]

            tensor = build_tensor( category_index )
        
            detect( 
                next_image = next_image, 
                on_no_objects = on_no_objects, 
                on_detected_objects = on_detected_objects, 
                config = config, 
                session = session, 
                tensor = tensor,
                constraint = detection_filter
            )
finally:
    camera.stop()
    
