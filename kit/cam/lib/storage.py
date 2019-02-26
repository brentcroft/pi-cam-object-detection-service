"""


"""
import os
import math
from PIL import ImageDraw
from PIL import ImageFont
"""


"""
from ground_truth import put_file_meta
from ground_truth import put_csv_meta

from util import switch_file
from util import datestamp
from util import log_message
from util import calculate_color
from util import complementary_color
"""


"""
def get_font( config, fonts={} ):

    # default is DejaVuSansMono.ttf
    name = config['FONT_NAME'] if 'FONT_NAME' in config else 'DejaVuSansMono.ttf'
    
    # default is 12
    size = config['FONT_SIZE'] if 'FONT_SIZE' in config else 12
    
    if name in fonts and size in fonts[ name ]:
        return fonts[ name ][ size ]
    try:
        font = ImageFont.truetype( name, size )  

        log_message( "Loaded font: name=[{}], size=[{}]".format( name, size ) )
        
        if name not in fonts:
            fonts[ name ] = {}
        fonts[ name ][ size ] = font
        
        return font
    except IOError:
        raise ValueError( "Font not available: name={}, size={}; use fc-list to find available fonts, then assign in 'cam.properties'.".format( name, size ) )
"""


"""
def draw_text_on_image( image=None, text=None, offset=( 5, 5 ), config=None ):

    # default is white
    bg_color = config['FONT_BG_COLOR'] if 'FONT_BG_COLOR' in config else 'white'
    
    # default is black
    fg_color = config['FONT_FG_COLOR'] if 'FONT_FG_COLOR' in config else 'black'
    
    font = get_font( config )
    
    draw = ImageDraw.Draw( image )
    
    text_width, text_height = font.getsize( text )

    margin = math.ceil( 0.05 * text_height )
    
    draw.rectangle( 
        [ 
            offset, 
            ( 
                text_width + offset[0] + ( 2 * margin ), 
                text_height + offset[1] + ( 2 * margin ) 
            )
        ], 
        fill=bg_color 
    )  
    
    draw.text( 
        ( offset[0] + margin, offset[1] + margin ), 
        text,
        fill=fg_color, 
        font=font 
    )
   
def draw_box_on_image( image=None, box=None, color='red', thickness=4, text="", config=None ):

    font = get_font( config )
    
    draw = ImageDraw.Draw( image )
    
    im_width, im_height = image.size

    left, right, top, bottom = ( box[0], box[2], box[1], box[3] )

    draw.line(
        [ (left, top), (left, bottom), (right, bottom), (right, top), (left, top)], 
        width=thickness, 
        fill=color
    )
    
    text_width, text_height = font.getsize( text )

    line_height = ( 1 + 2 * 0.05 ) * text_height

    if top > line_height:
        text_bottom = top
    else:
        text_bottom = bottom + line_height

    margin = math.ceil( 0.05 * text_height )
    
    draw.rectangle(
        [
            ( left, text_bottom - text_height - 2 * margin ), 
            ( left + text_width, text_bottom )
        ],
        fill = color
    )
    draw.text(
        ( left + margin, text_bottom - text_height - margin ),
        text,
        fill = complementary_color( color ),
        font = font
    )
"""


"""
def draw_objects_on_image( image=None, objects=None, thickness=4, config=None ):

    # default is 30
    min_channel = config['COLORS_MIN_CHANNEL'] if 'COLORS_MIN_CHANNEL' in config else 30
    
    # default is 120
    max_channel = config['COLORS_MAX_CHANNEL'] if 'COLORS_MAX_CHANNEL' in config else 120
    
    # default is False
    no_cache = config['COLORS_NO_CACHE'] if 'COLORS_NO_CACHE' in config else False

    # so higher scores draw last
    objects.sort( key = lambda x: x['score'] )
    
    for object in objects:
        class_name = object['name']
        class_score = object['score']
        class_color = calculate_color( class_name, min_channel=min_channel, max_channel=max_channel, no_cache=no_cache )

        draw_box_on_image( 
            image = image, 
            box = object['box'], 
            color = class_color, 
            thickness = thickness, 
            text = '{} {}%'.format( class_name, str( round( class_score * 100 ) ) ),
            config = config
        )
"""


"""
def store_image_and_detection_files( context=None, config=None):

    image_uri = context['uri']
    
    stored_paths = {}
    
    date_text = datestamp()
    
    if 'CALENDAR_IMAGE_STORE' in config and config['CALENDAR_IMAGE_STORE'] is not None:
        store_dir = os.path.join( config['CALENDAR_IMAGE_STORE'], date_text )
        if not os.path.exists( store_dir ):
            os.makedirs( store_dir )
        
        image_filename = "{}{}".format( image_uri, '.jpg' ) 
        image_file = os.path.join( store_dir, image_filename )

        if 'CALENDAR_IMAGE_RAW' in config and config['CALENDAR_IMAGE_RAW']:
            image, meta_data = context['raw']
        else:
            image, meta_data = context['frame']

        meta_data['size'] = ( image.width, image.height, 3 )  

        # put annotation
        draw_text_on_image( image=image, text=image_uri, config=config )     
        
        image.save( image_file )
        
        stored_paths[ 'calendar_image_file' ] = image_file
        
        # update meta data
        meta_data['folder'] = store_dir
        meta_data['filename'] = image_filename         


    if 'CALENDAR_DETECTION_STORE' in config and config['CALENDAR_DETECTION_STORE'] is not None:
        store_dir = os.path.join( config['CALENDAR_DETECTION_STORE'], date_text, config['GRAPH'] )
        if not os.path.exists( store_dir ):
            os.makedirs( store_dir )
            
        detection_file = os.path.join( store_dir, "{}{}".format( image_uri, '.xml' ) )

        if 'CALENDAR_IMAGE_RAW' in config and config['CALENDAR_IMAGE_RAW']:
            _, meta_data = context['raw']
        else:
            _, meta_data = context['frame']

            
        put_file_meta( detection_file, meta_data )
        stored_paths[ 'calendar_detection_file' ] = detection_file


        # relative image folder wrt this CSV file
        meta_data['folder'] = os.path.relpath( meta_data['folder'], config['CALENDAR_DETECTION_STORE'] )        
        csv_log_file = "{}_{}_log.csv".format( date_text, config['GRAPH'] )
        
        put_csv_meta( os.path.join( config['CALENDAR_DETECTION_STORE'], csv_log_file ), meta_data )
        

        
    if 'CURRENT_IMAGE_STORE' in config and config['CURRENT_IMAGE_STORE'] is not None:
        store_dir = config['CURRENT_IMAGE_STORE']
        if not os.path.exists( store_dir ):
            os.makedirs( store_dir )        
        
        # default is image
        image_name = config['CURRENT_IMAGE_NAME'] if 'CURRENT_IMAGE_NAME' in config else 'image'
        
        image_filename = "{}{}".format( image_name, '.jpg' )
        image_file = os.path.join( store_dir, image_filename )
        detection_file = os.path.join( store_dir, "{}{}".format( image_name, '.xml' ) )

        if 'CURRENT_IMAGE_RAW' in config and config['CURRENT_IMAGE_RAW']:
            image, meta_data = context['raw']
        else:
            image, meta_data = context['frame']
        
        
        # update meta data
        meta_data['size'] = ( image.width, image.height, 3 ) 
        meta_data['folder'] = store_dir
        meta_data['filename'] = image_filename          
        
        # save and switch as these files may be monitored
        temp_image_file = "{}.tmp.jpg".format( image_file )
        temp_detection_file = "{}.tmp.xml".format( detection_file )
        
        # put annotation
        draw_text_on_image( image=image, text=image_uri, config=config )
        
        image.save( temp_image_file )
        
        put_file_meta( temp_detection_file, meta_data )
        put_csv_meta( os.path.join( store_dir, "detections.csv" ), meta_data )
        
        switch_file( temp_image_file, image_file )        
        switch_file( temp_detection_file, detection_file )  

        stored_paths[ 'current_image_file' ] = image_file
        stored_paths[ 'current_detection_file' ] = detection_file        
        
    return stored_paths
"""

    Boxed images are always created alongside detection files and/or current image

"""
def store_boxed_image( context=None, stored_paths=None, meta_data=None, config=None ):

    if 'BOXED_IMAGES' in config and not config['BOXED_IMAGES']:
        return

    frame_coords = config['CURRENT_FRAME']
    
    # default is 4
    line_thickness = config['BOX_LINE_THICKNESS'] if 'BOX_LINE_THICKNESS' in config else 4      
    
    # default is False
    calendar_is_raw = ( 'CALENDAR_IMAGE_RAW' in config and config['CALENDAR_IMAGE_RAW'] )
    
    # default is False
    current_is_raw = ( 'CURRENT_IMAGE_RAW' in config and config['CURRENT_IMAGE_RAW'] )

    # flow milestones
    calendar_has_detection_frame = False
    calendar_has_boxes = False
    calendar_has_annotation = False

    image_annotation = context['uri']
    
    # boxed image alongside detection file in daily directory
    if stored_paths is not None and 'calendar_detection_file' in stored_paths:
    
        if calendar_is_raw:
            image, meta_data = context['raw']
            
            draw_box_on_image( image = image, box = frame_coords, color = '#ffffff', thickness = line_thickness, text = 'DETECTION FRAME', config = config )
            calendar_has_detection_frame = True
            
        else:
            image, meta_data = context['frame']    


        if meta_data is not None:
            draw_objects_on_image( image = image, objects = meta_data['objects'], thickness = line_thickness, config = config )
            calendar_has_boxes = True
    
    
        draw_text_on_image( image = image, text = image_annotation, config = config)
        calendar_has_annotation = True
    
        # alongside image
        boxed_image_path = stored_paths['calendar_detection_file'].split(".")[0] + "_boxed.jpg"
        image.save( boxed_image_path )



    # boxed image in CURRENT_IMAGE_STORE
    if 'CURRENT_IMAGE_STORE' in config and config['CURRENT_IMAGE_STORE'] is not None:
    
        store_dir = config['CURRENT_IMAGE_STORE']
        if not os.path.exists( store_dir ):
            os.makedirs( store_dir )        
        
        # default is image
        image_name = config['CURRENT_IMAGE_NAME'] if 'CURRENT_IMAGE_NAME' in config else 'image'
        
        image_filename = "{}{}".format( image_name, '_boxed.jpg' )
        boxed_image_path = os.path.join( store_dir, image_filename )
   
        if current_is_raw:
            image, meta_data = context['raw']
            
            if not calendar_has_detection_frame:
                draw_box_on_image( image = image, box = frame_coords, color = '#ffffff', thickness = line_thickness, text = 'DETECTION FRAME', config = config )
                
        else:
            image, meta_data = context['frame']
               

        if meta_data is not None:
            if calendar_is_raw != current_is_raw or not calendar_has_boxes:
                draw_objects_on_image( image = image, objects = meta_data['objects'], thickness = line_thickness, config = config )

        if calendar_is_raw != current_is_raw or not calendar_has_annotation:
            draw_text_on_image( image = image, text = image_annotation, config = config )


        # save and switch as this file may be monitored
        temp_file = "{}.tmp.jpg".format( boxed_image_path )
        image.save( temp_file )
        switch_file( temp_file, boxed_image_path )

        