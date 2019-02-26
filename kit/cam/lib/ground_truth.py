"""

    Read/write ground truth meta-data to XML files.
    Extended Pascal/VOC format with additional attributes
   
"""
from lxml import etree as ET
from os.path import isfile
from util import timestamp
"""

    None becomes the empty string
"""
def write_attributes_to_element( parent_element, attributes, use_attributes_element = True, use_attribute_element = True ):
    if attributes is not None and len( attributes ) > 0:
        if use_attributes_element:
            attributes_element = ET.SubElement( parent_element, 'attributes')
        else:
            attributes_element = parent_element

        for attr in attributes:
            if use_attribute_element:
                attribute_element = ET.SubElement( attributes_element, 'attribute')
                attribute_element.set( "key", attr )
            else:
                attribute_element = ET.SubElement( attributes_element, attr )
            
            value = "" if attributes[ attr ] is None else str( attributes[ attr ] ) 
            attribute_element.text = str( value )
"""


"""
def maybe_number(value):
    try:
        try:
            return int(value)
        except:
            return float(value)
    except:
        return value
"""

    the empty string becomes None
"""
def read_attributes_from_element( parent_element, attributes={} ):
    try:
        attributes_element = parent_element.find("attributes")
        if attributes_element is not None:
            for attribute_element in attributes_element.findall("attribute"):
                value = attribute_element.text
                if value == "" or value == "None":
                    value = None
                attributes[ attribute_element.get( "key" ) ] = maybe_number( value )
    except Exception as e:
        raise ValueError( "Failed to read attributes: {}".format( e ) )
    return attributes
"""


"""
def get_file_meta( classification_file ):
    root = ET.parse( classification_file ).getroot()
    
    file_attributes = {}
    read_attributes_from_element( root, file_attributes )
    
    filename = root.find('filename').text
    
    if root.find('folder') is None:
        folder = None
    else:
        folder =  root.find('folder').text
        
    if root.find('path') is None:
        path = None 
    else:
        path = root.find('path').text
    
    size = root.find('size')
    width, height, depth = int(size.find('width').text), int(size.find('height').text), int(size.find('depth').text)
    item = 0    
    labeled_objects = []
    for member in root.findall('object'):
        class_name = member.find('name').text
        if member.find('score') is None:
            score = 0
        else:
            score = float( member.find('score').text )
        category_box = member.find( 'bndbox' )
        
        object_attributes = read_attributes_from_element( member )
        
        category_object = { 
            "name": class_name, 
            "box": ( 
                int(category_box[0].text), 
                int(category_box[1].text), 
                int(category_box[2].text), 
                int(category_box[3].text)
            ),
            "score": score,
            "item": item,
            "attributes": object_attributes
        }
        labeled_objects.append( category_object )
        item = item + 1

    return {
        "filename": filename,
        "folder": folder,
        "path": path,
        "size": ( width, height, depth ),
        "objects": labeled_objects,
        "attributes": file_attributes
    }
"""

    write a new classification file from meta-data
"""
def put_file_meta( classification_file, meta_data ):
    root = ET.Element( 'annotation' )
    
    if 'folder' in meta_data:
        ET.SubElement( root, 'folder' ).text = meta_data['folder']
        
    if 'filename' in meta_data:
        ET.SubElement( root, 'filename' ).text = meta_data['filename']
    
    if "path" in meta_data:
        ET.SubElement( root, 'path' ).text = meta_data['path']

    if "size" in meta_data:
        sizeE = ET.SubElement( root, 'size' )
        widthE, heightE, depthE = \
                ET.SubElement( sizeE, 'width' ), \
                ET.SubElement( sizeE, 'height' ), \
                ET.SubElement( sizeE, 'depth' )
        
        size = meta_data['size']
        widthE.text = str( size[0] ) 
        heightE.text = str( size[1] )
        depthE.text = str( size[2] ) 

        
    for item in meta_data["objects"]:
        try:
            objectE = ET.SubElement( root, 'object' )
            
            ET.SubElement( objectE, 'name' ).text = item["name"]

            xmin, ymin, xmax, ymax = item["box"]

            if 'score' in item and item["score"] is not None:
                ET.SubElement( objectE, 'score' ).text = str( item["score"] )

            # create elements
            bndboxE = ET.SubElement( objectE, 'bndbox' )
            xminE, yminE = ET.SubElement( bndboxE, 'xmin' ), ET.SubElement( bndboxE, 'ymin' )
            xmaxE, ymaxE = ET.SubElement( bndboxE, 'xmax' ), ET.SubElement( bndboxE, 'ymax' )


            bndboxE[0].text = str( xmin )
            bndboxE[1].text = str( ymin )
            bndboxE[2].text = str( xmax )
            bndboxE[3].text = str( ymax ) 
            
            if "attributes" in item:
                write_attributes_to_element( objectE, item["attributes"])

        except Exception as e:
            print( "BAD_OBJECT: {}\n {}".format( item, e ) )
            raise e
    
    if "attributes" in meta_data:
        write_attributes_to_element( root, meta_data["attributes"] )
    
    root.getroottree().write( classification_file, pretty_print=True )

    

def put_csv_meta( csv_file=None, meta_data=None ):
    header = None if isfile( csv_file ) else [
            "timestamp",
            "folder",
            "filename",
            "width", 
            "height", 
            "item",
            "name", 
            "xmin", 
            "ymin",
            "xmax",            
            "ymax", 
            "score" 
        ]
    
    # common for all objects in meta_data
    size = meta_data['size']
    folder, filename, width, height = meta_data['folder'], meta_data['filename'], str( int( size[0] ) ), str( int( size[1] ) ),         

    event_timestamp = timestamp()
    
    lines = []
    item_no = 1
    for item in meta_data["objects"]:
        lines += [ [ 
                event_timestamp, 
                folder, 
                filename, 
                width, height, 
                str( item_no ), 
                item["name"] 
            ] + [ 
                str( int( b ) ) for b in item["box"] 
            ] + [ 
                str( float( item['score'] ) ) 
            ] ]
        item_no += 1
            
            
            
    with open( csv_file, 'a' ) as f:  
        if header is not None:
            f.write( "{}\n".format( ", ".join( header ) ) )
        for line in lines:    
            f.write( "{}\n".format( ", ".join( line ) ) ) 


    