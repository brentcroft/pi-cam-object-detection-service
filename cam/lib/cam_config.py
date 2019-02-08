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
    sp = read_service()
    if 'SUSPENDED' in sp and sp['SUSPENDED'] == "1":
        raise ValueError( "Service was suspended!" )
    if 'DISABLED' in sp and sp['DISABLED'] == "1":
        raise ValueError( "Service is disabled!" )
"""


"""

def read_config( log = False ):
    props = Properties()
    with open( "cam.properties", "r" ) as f:
        props.load( f )

    config = {}

    # process
    config['MAX_SEQ'] = eval( props[ 'MAX_SEQ' ] ) if 'MAX_SEQ' in props else 10000
    config['LOG_FREQ'] = eval( props[ 'LOG_FREQ' ] ) if 'LOG_FREQ' in props else 50

    
    # camera
    config['CAM_IMAGE_RESOLUTION'] = eval( props[ 'CAM_IMAGE_RESOLUTION' ] ) if 'CAM_IMAGE_RESOLUTION' in props else [ 1920, 1080 ]
    config['CAM_IMAGE_ROTATION'] = eval( props[ 'CAM_IMAGE_ROTATION' ] ) if 'CAM_IMAGE_ROTATION' in props else 0

    
    # what TF graph
    config['GRAPHS'] = props[ 'GRAPHS' ]
    config['GRAPH'] = props[ 'GRAPH' ]
    config['GRAPH_RESOLUTION'] = eval( props[ 'GRAPH_RESOLUTION' ] ) if 'GRAPH_RESOLUTION' in props else None
    config['NUM_CLASSES'] = int( props[ 'NUM_CLASSES' ] )
    config['USE_FROZEN_GRAPH'] = props[ 'USE_FROZEN_GRAPH' ].lower() == 'true' if 'USE_FROZEN_GRAPH' in props else False    
    config['RECACHE_GRAPH'] = props[ 'RECACHE_GRAPH' ].lower() == 'true' if 'RECACHE_GRAPH' in props else False

        
    # what aperture to use for detection
    config['DETECTION_ORIGIN'] = eval( props[ 'DETECTION_ORIGIN' ] ) if 'DETECTION_ORIGIN' in props else None
    config['DETECTION_APERTURE'] = eval( props[ 'DETECTION_APERTURE' ] ) if 'DETECTION_APERTURE' in props else [ 1920, 1080 ]

    # if origin in None then put aperture in centre of cam resolution
    if config['DETECTION_ORIGIN'] is None:
        dw, dh = config['DETECTION_APERTURE']
        crw, crh = config['CAM_IMAGE_RESOLUTION']
        dox, doy = ( crw - dw ) / 2, ( crh - dh ) / 2 
        config['DETECTION_FRAME'] = [ dox , doy, dox + dw, doy + dh ]
        #print( "Auto-centred DETECTION_FRAME: {}", config['DETECTION_FRAME'] )
    else:
        dox, doy = config['DETECTION_ORIGIN']
        dw, dh = config['DETECTION_APERTURE']
        config['DETECTION_FRAME'] = [ dox , doy, dox + dw, doy + dh ]
        #print( "Calculated DETECTION_FRAME: {}", config['DETECTION_FRAME'] )
    
    
    # constraints on detections
    config['MIN_SCORE'] = float( props[ 'MIN_SCORE' ] ) if 'MIN_SCORE' in props else 0.1 
    config['CLASS_MIN_SCORE'] = eval( props[ 'CLASS_MIN_SCORE' ] ) if 'CLASS_MIN_SCORE' in props else {}
    config['MAX_BOX_RATIO'] = float( props[ 'MAX_BOX_RATIO' ] ) if 'MAX_BOX_RATIO' in props else 0.5 
    config['MIN_BOX_RATIO'] = float( props[ 'MIN_BOX_RATIO' ] ) if 'MIN_BOX_RATIO' in props else 0.05 
    config['MAX_BOX_DEVIATION'] = float( props[ 'MAX_BOX_DEVIATION' ] ) if 'MAX_BOX_DEVIATION' in props else 0.1 
    

    
    # outputs
    storage_type = props['STORAGE'] if 'STORAGE' in props else 'RAW'
    
    config['STORAGE'] = 1 if 'frame' == storage_type.lower() else 0
    
    config['CURRENT_IMAGE_STORE'] = props[ 'CURRENT_IMAGE_STORE' ] if 'CURRENT_IMAGE_STORE' in props else None
    config['CURRENT_IMAGE_NAME'] = props[ 'CURRENT_IMAGE_NAME' ] if 'CURRENT_IMAGE_NAME' in props else 'image'
    
    config['CALENDAR_IMAGE_STORE'] = props[ 'CALENDAR_IMAGE_STORE' ] if 'CALENDAR_IMAGE_STORE' in props else None
    config['CALENDAR_DETECTION_STORE'] = props[ 'CALENDAR_DETECTION_STORE' ] if 'CALENDAR_DETECTION_STORE' in props else None
    
    
    #
    config['BOX_TRACKER'] = props['BOX_TRACKER'].lower() == 'true' if 'BOX_TRACKER' in props else False
    config['BOX_TRACKER_RATIOS'] = eval( props['BOX_TRACKER_RATIOS'] ) if 'BOX_TRACKER_RATIOS' in props else [ 8, 8 ]    
    
    #   
    config['BOXED_IMAGES'] = props[ 'BOXED_IMAGES' ].lower() == 'true' if 'BOXED_IMAGES' in props else False
    config['LINE_THICKNESS'] = int( props[ 'LINE_THICKNESS' ] ) if 'LINE_THICKNESS' in props else 5
        
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

    graph_filename = 'frozen_inference_graph.pb' if config['USE_FROZEN_GRAPH'] else 'inference_graph.pb'
    labels_filename = 'object-detection.pbtxt' 
    
    cache_dir = join( '.', config['GRAPH'] )

    # check for local cached graph
    CACHED_GRAPH = join( cache_dir, graph_filename )
    CACHED_LABELS = join( cache_dir, labels_filename )

    if config['RECACHE_GRAPH'] or not exists( CACHED_GRAPH ) or not exists( CACHED_LABELS ):

        # Path to frozen detection graph
        PATH_TO_CKPT = join( config['GRAPHS'], config['GRAPH'], graph_filename )

        # protobuf of categories
        PATH_TO_LABELS = join( config['GRAPHS'], config['GRAPH'], labels_filename )

        # do checks
        if not exists( PATH_TO_CKPT ):
            raise ValueError( "Graph: {} does not exist.".format( PATH_TO_CKPT ) )

        if not exists( PATH_TO_LABELS ):
            raise ValueError( "Graph Labels: {} does not exist.".format( PATH_TO_LABELS ) )

        if not exists( cache_dir ):
            makedirs( cache_dir )         
            
        copyfile( PATH_TO_CKPT, CACHED_GRAPH )
        copyfile( PATH_TO_LABELS, CACHED_LABELS )

    return ( CACHED_GRAPH, CACHED_LABELS )    