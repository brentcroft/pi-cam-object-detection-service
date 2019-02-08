import numpy as np
import time
import os
import tensorflow as tf

import traceback

import ntpath

import traceback
import platform


from collections import defaultdict
from io import StringIO
from PIL import Image

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

from util import log_message
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

    build input and output tensors
    also packing in the category index
    
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

    Given a data object which represents theresults of detection 
    then get a list of boxes with extra dimensions for score, class name and index.

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
        box_raw = boxes[i].tolist()
        box = [ box_raw[1], box_raw[0], box_raw[3], box_raw[2] ]
        
        if constraint is None or constraint( class_name, score, box, frame ):
            objects.append( [ 
                x_off + int( round( box[0] * frame_width ) ), 
                y_off + int( round( box[1] * frame_height ) ), 
                x_off + int( round( box[2] * frame_width ) ), 
                y_off + int( round( box[3] * frame_height ) ), 
                scores[i],
                str( class_name ), 
                i
            ] )
    return objects    
"""

    run the graph on the image and process any results
    returning details of detected objects

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
def next_detected_image( 
            next_image=None, 
            on_no_objects=None, 
            config=None, 
            session=None, 
            tensor=None,
            constraint=None
        ):
        
    max_seq = config['MAX_SEQ'] if 'MAX_SEQ' in config else 100 
    log_freq = config['LOG_FREQ'] if 'LOG_FREQ' in config else 10
        
    detected_objects = []
    seq = 0
    start_time = time.time() 
    
    while not detected_objects:
        seq = seq + 1
        
        image_uri, raw_image  = next_image()
        
        if raw_image is None:
            raise ValueError( "No image nor uri were returned." )

        frame_coords = config['CURRENT_FRAME']
        frame_image = raw_image.crop( frame_coords )            
    
        detected_objects = detect_objects( 
            frame_image, 
            frame_coords, 
            config, 
            session, 
            tensor, 
            constraint 
        )

        if not detected_objects:
            on_no_objects( image_uri, raw_image, frame_image )
        
        if (seq % log_freq) == 0:
            log_stats( "Unclassified", start_time, seq, max_seq )
        
        if seq >= max_seq:
            raise GaveUpWaitingException( "Hit max. seq [{}], retiring.".format( seq ) )

    # convert to GT format
    # boxes relative to raw
    # boxes as lists since we might move the box
    meta_data = { 
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
    return [ seq, image_uri, raw_image, frame_image, meta_data ]
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
    log_message( "{}: [{} of {}] {}s [{} s/i, {} i/s].".format( prefix, item_no, total_no, round( duration, 2), s_per_i, i_per_s ) )        
"""


"""
def detect( 
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
        seq, image_uri, raw_image, frame_image, meta_objects = next_detected_image( 
            next_image = next_image, 
            on_no_objects = on_no_objects, 
            config = config, 
            session = session, 
            tensor = tensor,
            constraint = constraint
        )
        
        end_time = time.time()
        duration = ( end_time - start_time )

        i_per_s = 0
        s_per_i = 0
        if duration > 0 and seq > 0:
            i_per_s = round( seq / duration, 3 )
            s_per_i = round( duration / seq, 3 )

        stats = ( len( meta_objects ), round( duration, 2 ), s_per_i, i_per_s )
            
        # callback for detected objects
        on_detected_objects( seq, image_uri, raw_image, frame_image, meta_objects, stats )

"""


"""
def draw_objects_on_image( image, objects, class_colors, line_thickness ):
    # so higher scores draw last
    objects.sort( key = lambda x: x['score'])
    for object in objects:
        class_name = object['name']
        class_score = object['score']
        if class_name in class_colors:
            class_color = class_colors[ class_name ]
        else:
            print( "No class color for category: {}".format( class_name ) )
            class_color = 'yellow'

        # note unusual order of co-ords
        b2, b1, b4, b3 = object['box']
        
        vis_util.draw_bounding_box_on_image(
            image, 
            b1, b2, b3, b4,
            color=class_color, 
            thickness = line_thickness,
            display_str_list = [ '{} {}%'.format( class_name, str( round( class_score * 100 ) ) ) ],
            use_normalized_coordinates = False )         