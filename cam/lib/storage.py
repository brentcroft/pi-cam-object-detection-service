import os
from ground_truth import put_file_meta
from detection import draw_objects_on_image
from util import switch_file
from util import datestamp
"""


"""
def store_image_and_detection_files( image_uri=None, image=None, meta_data=None, config=None):

    stored_paths = {}
    
    if config['CALENDAR_IMAGE_STORE'] is not None:
        store_dir = os.path.join( config['CALENDAR_IMAGE_STORE'], datestamp() )
        if not os.path.exists( store_dir ):
            os.makedirs( store_dir )
        
        image_filename = "{}{}".format( image_uri, '.jpg' ) 
        image_file = os.path.join( store_dir, image_filename )

        image.save( image_file )
        
        stored_paths[ 'calendar_image_file' ] = image_file
        
        # update meta data
        meta_data['folder'] = store_dir
        meta_data['filename'] = image_filename         


    if config['CALENDAR_DETECTION_STORE'] is not None:
        store_dir = os.path.join( config['CALENDAR_DETECTION_STORE'], datestamp(), config['GRAPH'] )
        if not os.path.exists( store_dir ):
            os.makedirs( store_dir )
            
        detection_file = os.path.join( store_dir, "{}{}".format( image_uri, '.xml' ) )
        
        put_file_meta( detection_file, meta_data )
        
        stored_paths[ 'calendar_detection_file' ] = detection_file

        
    if config['CURRENT_IMAGE_STORE'] is not None:
        store_dir = config['CURRENT_IMAGE_STORE']
        if not os.path.exists( store_dir ):
            os.makedirs( store_dir )        
        
        image_name = config['CURRENT_IMAGE_NAME']
        image_filename = "{}{}".format( image_name, '.jpg' )
        image_file = os.path.join( store_dir, image_filename )
        detection_file = os.path.join( store_dir, "{}{}".format( image_name, '.xml' ) )
        
        stored_paths[ 'current_image_file' ] = image_file
        stored_paths[ 'current_detection_file' ] = detection_file
        
        # update meta data
        meta_data['folder'] = store_dir
        meta_data['filename'] = image_filename          
        
        # save and switch as these files may be monitored
        temp_image_file = "{}.tmp.jpg".format( image_file )
        temp_detection_file = "{}.tmp.xml".format( detection_file )
        
        image.save( temp_image_file )
        put_file_meta( temp_detection_file, meta_data )
        
        switch_file( temp_image_file, image_file )        
        switch_file( temp_detection_file, detection_file )        
        
    return stored_paths
    
    
"""
    Boxed images are created alongside detection files
"""
def store_boxed_image( image=None, stored_paths=None, meta_data=None, config=None ):

    if not config['BOXED_IMAGES']:
        return

    frame_coords, line = config['CURRENT_FRAME'], config['LINE_THICKNESS']        
        
    if meta_data is not None:
        draw_objects_on_image( image, meta_data['objects'], line )
    
    #draw frame if raw
    if config['STORAGE'] == 0:
        draw_objects_on_image( image, [ { 'name': 'frame', 'score': 0, 'box': frame_coords } ], line )

    # boxed image alongside detection file in daily directory
    if stored_paths is not None and 'calendar_detection_file' in stored_paths:
        image.save( stored_paths['calendar_detection_file'].split(".")[0] + "_boxed.jpg" )
        
    #
    if config['CURRENT_IMAGE_STORE'] is not None:
        store_dir = config['CURRENT_IMAGE_STORE']
        if not os.path.exists( store_dir ):
            os.makedirs( store_dir )        
        
        image_name = config['CURRENT_IMAGE_NAME']
        image_filename = "{}{}".format( image_name, '_boxed.jpg' )    
        boxed_image_path = os.path.join( store_dir, image_filename )

        # save and switch as this file may be monitored
        temp_file = "{}.tmp.jpg".format( boxed_image_path )
        image.save( temp_file )
        switch_file( temp_file, boxed_image_path )

        