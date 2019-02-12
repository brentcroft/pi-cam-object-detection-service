"""

"""
import time
import traceback
import numpy as np
from copy import deepcopy
"""

"""
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
"""

"""
from boxes import boxes_move
from util import log_message
from util import calculate_color
"""

    initialise a graph from files

""" 
def init_graph( graph_path=None, labels_path=None, num_classes=0 ):

    log_message( 'Using Tensorflow: ' + tf.__version__ )

    label_map = label_map_util.load_labelmap( labels_path )
    categories = label_map_util.convert_label_map_to_categories( label_map, max_num_classes=num_classes, use_display_name=True )
    category_index = label_map_util.create_category_index( categories )

    detection_graph = tf.Graph()

    with detection_graph.as_default():
      od_graph_def = tf.GraphDef()
      with tf.gfile.GFile( graph_path, 'rb' ) as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    log_message( "Loaded graph=[{}]".format( graph_path ) )
    log_message( "Loaded categories=[{}]".format( labels_path ) )
        
    return [ detection_graph, label_map, categories, category_index ]  
"""

    Build input and output tensors
    also packing in the category index.
    
    The key names work for SSD Mobilenet derivatives, not sure how valid for other graph families.
    
"""
def build_tensor( category_index ):
    # Get handles to input and output tensors
    ops = tf.get_default_graph().get_operations()
    all_tensor_names = {output.name for op in ops for output in op.outputs}
    
    # build a tensor dictionary
    tensor_dict = {}
    
    for key in [
        'num_detections', 'detection_boxes', 'detection_scores',
        'detection_classes', 'detection_masks'
    ]:
        tensor_name = key + ':0'
        if tensor_name in all_tensor_names:
            tensor_dict[key] = tf.get_default_graph().get_tensor_by_name( tensor_name )

    # load the image tensor
    image_tensor_key = 'image_tensor:0'
    image_tensor = tf.get_default_graph().get_tensor_by_name( image_tensor_key )

    
    # package and return
    return [ tensor_dict, image_tensor, category_index ]    
"""

    Extract detections from graph output tensors.

"""    
def extract_objects( 
        data=None, 
        category_index=None, 
        image_dim=None, 
        frame=None,
        constraint=None 
        ):
   
    boxes = data['detection_boxes']
    classes = data['detection_classes']
    scores = data['detection_scores']

    imageWidth, imageHeight, imageDepth = image_dim  
    
            
    x_off, y_off = ( frame[0], frame[1] )
    frame_width, frame_height = ( frame[2] - x_off, frame[3] - y_off )

    objects = []
    
    num_boxes = 0
    
    # create objects
    for i in range( boxes.shape[0] ):
        
        # get classname
        if classes[i] in category_index.keys():
            class_name = category_index[classes[i]]['name']
        else:
            class_name = "N/A [{}]".format( classes[i], i )

        # confidence score for this box
        score = scores[i]
        
        # switch back to conventional order
        # and resize with respect to frame
        box_raw = boxes[i].tolist()
        box = [ 
            x_off + int( round( box_raw[1] * frame_width ) ), 
            y_off + int( round( box_raw[0] * frame_height ) ),
            x_off + int( round( box_raw[3] * frame_width ) ),
            y_off + int( round( box_raw[2] * frame_height ) )
        ]
        
        if constraint is None or constraint( class_name, score, box, frame ):
            objects.append( [ box[0], box[1], box[2], box[3], scores[i], str( class_name ), i ] )
    return objects    
"""

    Apply the graph on the image and extract detections from the output tensors.
    Return detections.

"""
def detect_objects( image, frame_coords, config, session, tensor, constraint ):

    tensor_dict, image_tensor, category_index = tensor
            
    detected_objects = []

    try:
        inference_results_dict = session.run( tensor_dict, feed_dict={ image_tensor: np.expand_dims( image, 0 ) } )
        
        # all outputs are float32 numpy arrays, so convert types as appropriate
        inference_results_dict['num_detections'] = int(inference_results_dict['num_detections'][0])
        inference_results_dict['detection_classes'] = inference_results_dict[ 'detection_classes'][0].astype(np.uint8)
        inference_results_dict['detection_boxes'] = inference_results_dict['detection_boxes'][0]
        inference_results_dict['detection_scores'] = inference_results_dict['detection_scores'][0]  
    
        extracted_objects = extract_objects( 
            data = inference_results_dict, 
            category_index = category_index, 
            image_dim = ( image.width, image.height, 3 ),
            frame = frame_coords,
            constraint = constraint
        )

        if extracted_objects:
            detected_objects.extend( extracted_objects )

    except Exception as e:
        log_message( "Ignoring bad image: {}".format( e ) )
        print( traceback.format_exc() )
        
        return []
    
    return detected_objects
"""
    

"""
def log_stats( prefix, start_time, item_no, total_no ):
    end_time = time.time()
    duration = ( end_time - start_time )
    i_per_s = 0
    s_per_i = 0
    if duration > 0 and item_no > 0:
        i_per_s = round( item_no / duration, 3 )
        s_per_i = round( duration / item_no, 3 )
    log_message( "{}: [{}/{}] {}s [{} s/i, {} i/s].".format( prefix, item_no, total_no, round( duration, 2), s_per_i, i_per_s ) )        
"""

    Request an image until there are detections.
    Notify on no detections return on detections.   

"""
def next_detected_image( 
            next_image=None, 
            on_no_objects=None, 
            config=None, 
            session=None, 
            tensor=None,
            constraint=None
        ):
        
    detected_objects = []
    seq = 0
    start_time = time.time() 
    
    while not detected_objects:
        seq = seq + 1
        
        context = next_image()
        context['seq'] = seq
        
        if 'raw' not in context or context['raw'] is None or len( context['raw'] ) == 0:
            raise ValueError( "No image nor uri were returned." )

        raw_image, _ = context['raw']
            
        frame_coords = config['CURRENT_FRAME']
        
        frame_image = raw_image.crop( frame_coords )

        context['frame'] = ( frame_image, None )
    
        detected_objects = detect_objects( 
            frame_image, 
            frame_coords, 
            config, 
            session, 
            tensor, 
            constraint 
        )

        if not detected_objects:
            on_no_objects( context )

        # default is 10
        log_freq = config['LOG_UNDETECTED_FREQ'] if 'LOG_UNDETECTED_FREQ' in config else 10  
        
        # default is True
        log_undetected = config['LOG_UNDETECTED'] if 'LOG_UNDETECTED' in config else True
        
        if log_undetected and ( seq % log_freq ) == 0:
            log_stats( "Undetected", start_time, seq, max_seq )
        
        
        # default is 100
        max_seq = config['LOG_UNDETECTED_MAX_SEQ'] if 'LOG_UNDETECTED_MAX_SEQ' in config else 100 
        
        if seq >= max_seq:
            raise ValueError( "Hit max. seq [{}], retiring.".format( seq ) )

    # convert to GT format
    # boxes relative to raw
    # boxes as lists since we might move the box
    raw_meta_data = { 
        'objects': [ 
            { 
                'box': [ dto[0], dto[1], dto[2], dto[3] ],
                'score': dto[4],
                'name':  dto[5],
                'index': dto[6]
            }
            for dto in detected_objects
        ]
    }
    
    context['raw'] = ( raw_image, raw_meta_data )
    
    frame_meta_data = deepcopy( raw_meta_data )
    
    boxes_move( 
        boxes = [ object['box'] for object in frame_meta_data['objects'] ], 
        displacement = config['CURRENT_FRAME'], 
        subtract = True 
    )    
    
    context['frame'] = ( frame_image, frame_meta_data )
    
    return context
"""

    Request and store images and detections.
    
"""
def detect_forever( 
            next_image=None, 
            on_no_objects=None, 
            on_detected_objects=None, 
            config=None, 
            session=None, 
            tensor=None,
            constraint=None
        ):

    while True:        
        start_time = time.time()    
        
        # blocks until have objects or max_seq
        context = next_detected_image( 
            next_image = next_image, 
            on_no_objects = on_no_objects, 
            config = config, 
            session = session, 
            tensor = tensor,
            constraint = constraint
        )
        
        
        do_stats = True
 
        if do_stats:
            num_detections = len( context['raw'][1] ) if len( context['raw'] ) > 0 else 0
            
            end_time = time.time()
            duration = ( end_time - start_time )

            i_per_s = 0
            s_per_i = 0
            
            seq = context['seq']
            
            if duration > 0 and seq > 0:
                i_per_s = round( seq / duration, 3 )
                s_per_i = round( duration / seq, 3 )

            context['stats'] = ( num_detections, round( duration, 2 ), s_per_i, i_per_s )
        
        on_detected_objects( context )
