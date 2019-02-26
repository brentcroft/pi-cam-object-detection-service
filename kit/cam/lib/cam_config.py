"""


"""
import json

from os.path import join
from os.path import exists
from os import makedirs

from shutil import copyfile

from properties import Properties
from util import log_message
"""


"""
def read_service():
    service_props = Properties()
    with open( "service.properties", "r" ) as f:
        service_props.load( f )
    return service_props
"""


"""
def check_service():
    service = read_service()
    if 'SUSPENDED' in service and service['SUSPENDED'] == "1":
        raise ValueError( "Service was suspended!" )
    return service
"""


"""
def read_config( log = False ):
    props = Properties()
    with open( "cam.properties", "r" ) as f:
        props.load( f )

    config = {}
    
    props.set_bool_or( config, 'NO_RELOAD' )
    
    
    # camera
    props.set_eval_or( config, 'CAMERA_RESOLUTION', [ 720, 405 ] )
    props.set_eval_or( config, 'CAMERA_ROTATION', 0 )

    # what TF graph
    props.set_text_or( config, 'GRAPH_SERVER' )
    config['GRAPH'] = props[ 'GRAPH' ]
    config['GRAPH_NUM_CLASSES'] = int( props[ 'GRAPH_NUM_CLASSES' ] )
    
    props.set_text_or( config, 'GRAPH_FILENAME', 'frozen_inference_graph.pb' )
    props.set_text_or( config, 'GRAPH_LABELS_FILENAME', 'object-detection.pbtxt' ) 

    #
    props.set_eval_or( config, 'GRAPH_RESOLUTION' )
    props.set_bool_or( config, 'RECACHE_GRAPH' )

        
    # what aperture to use for detection
    props.set_eval_or( config, 'DETECTION_ORIGIN' )
    props.set_eval_or( config, 'DETECTION_APERTURE', [ 480, 270 ] )

    # if not origin then put aperture in centre of cam resolution
    if 'DETECTION_ORIGIN' in config:
        dox, doy = config['DETECTION_ORIGIN']
        dw, dh = config['DETECTION_APERTURE']
        config['DETECTION_FRAME'] = [ dox , doy, dox + dw, doy + dh ]
    else:
        dw, dh = config['DETECTION_APERTURE']
        crw, crh = config['CAMERA_RESOLUTION']
        dox, doy = ( crw - dw ) / 2, ( crh - dh ) / 2 
        config['DETECTION_FRAME'] = [ dox , doy, dox + dw, doy + dh ]
    
    
    # logging
    props.set_bool_or( config, 'LOG_DETECTIONS' )    
    props.set_bool_or( config, 'LOG_REJECTIONS' )
    props.set_bool_or( config, 'LOG_UNDETECTED' )
    props.set_int_or( config, 'LOG_UNDETECTED_FREQ' )
    
    # quit after this many undetections
    props.set_int_or( config, 'UNDETECTED_MAX_SEQ' )
    
    # constraints on detections
    props.set_float_or( config, 'DETECTION_MIN_SCORE' ) 
    props.set_eval_or( config, 'DETECTION_CLASS_MIN_SCORE' ) 
    props.set_float_or( config, 'BOX_DIM_MAX_DEVIATION' ) 
    props.set_eval_or( config, 'BOX_DIM_MAX_RATIO' )    
    props.set_eval_or( config, 'BOX_AREA_MIN_MAX_RATIO' )    


    
    # outputs
    props.set_text_or( config, 'CURRENT_IMAGE_STORE' )
    props.set_text_or( config, 'CALENDAR_IMAGE_STORE' )
    
    if 'CURRENT_IMAGE_STORE' in config:
        props.set_bool_or( config, 'CURRENT_IMAGE_RAW' )
        props.set_text_or( config, 'CURRENT_IMAGE_NAME' )
        props.set_int_or( config, 'CURRENT_IMAGE_PORT' )

    if 'CALENDAR_IMAGE_STORE' in config:
        props.set_bool_or( config, 'CALENDAR_IMAGE_RAW' )
        props.set_text_or( config, 'CALENDAR_DETECTION_STORE', config['CALENDAR_IMAGE_STORE'] )

        
    props.set_bool_or( config, 'COLORS_NO_CACHE' )
    props.set_int_or( config, 'COLORS_MAX_CHANNEL' )
    props.set_int_or( config, 'COLORS_MIN_CHANNEL' )

    #
    props.set_bool_or( config, 'BOX_TRACKER' )
    props.set_eval_or( config, 'BOX_TRACKER_RATIOS' )    
    
    #   
    props.set_bool_or( config, 'BOXED_IMAGES' )
    props.set_int_or( config, 'BOX_LINE_THICKNESS' )
    
    #
    props.set_text_or( config, 'FONT_NAME' )
    props.set_int_or( config, 'FONT_SIZE' )
    props.set_text_or( config, 'FONT_BG_COLOR' )
    props.set_text_or( config, 'FONT_FG_COLOR' )
    
        
    if log:
        log_message( get_config_text( config ) )    
        
    return config
    
def to_json( object ):
    return json.dumps( object, sort_keys=True, separators=( ', ', ':' ), indent=4 )


def get_config_text( config ):

    report = "Pi_Cam_Object_Detector:"
    
    for key, value in sorted([ ( k, v ) for k, v in config.items() ], key=lambda e: e[0] ):
        if value is not None:
            report += "\n  {}: {}".format( key, value )
        
    return report

    
def maybe_cache_graph( config=None ):

    graph_filename = config['GRAPH_FILENAME']
    labels_filename = config['GRAPH_LABELS_FILENAME']
    
    recache_graph = 'RECACHE_GRAPH' in config and config['RECACHE_GRAPH']

    if 'GRAPH' not in config:
        raise ValueError( "Failed to cache graph: {}".format( "'GRAPH' not in config" ) )
    
    graph_dir = config['GRAPH']
    
    cache_dir = join( '.', graph_dir )

    # check for local cached graph
    cached_graph_file = join( cache_dir, graph_filename )
    cached_labels_file = join( cache_dir, labels_filename )

    if recache_graph or not ( exists( cached_graph_file ) and exists( cached_labels_file ) ):

        if 'GRAPH_SERVER' not in config:
            raise ValueError( "Failed to cache graph: {}".format( "'GRAPH_SERVER' not in config" ) )
            
        graph_server = config['GRAPH_SERVER']
    
        # Path to frozen detection graph
        server_graph_file = join( graph_server, graph_dir, graph_filename )
        server_labels_file = join( graph_server, graph_dir, labels_filename )

        # do checks
        if not exists( server_graph_file ):
            raise ValueError( "Graph: {} does not exist.".format( server_graph_file ) )

        if not exists( server_labels_file ):
            raise ValueError( "Graph Labels: {} does not exist.".format( server_labels_file ) )

        if not exists( cache_dir ):
            makedirs( cache_dir )         
            
        copyfile( server_graph_file, cached_graph_file )
        copyfile( server_labels_file, cached_labels_file )

    return ( cached_graph_file, cached_labels_file )    