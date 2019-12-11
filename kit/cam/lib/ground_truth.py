"""

    Read/write ground truth meta-data to XML files.
    Extended Pascal/VOC format with additional attributes

"""
from lxml import etree as ET
from os.path import isfile
from util import timetext
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
def get_object_meta( element, item=0 ):
    box = element.find( 'bndbox' )
    object_meta = {
        "box": (
            int(box[0].text),
            int(box[1].text),
            int(box[2].text),
            int(box[3].text)
        ),
        "name": "(none)" if element.find('name') is None else element.find('name').text,
        "score": 0.0 if element.find('score') is None else float( element.find('score').text ),
        "item": item,
        "attributes": read_attributes_from_element( element )
    }

    predecessor = element.find( 'predecessor' )
    if predecessor is not None:
        object_meta['predecessor'] =  get_object_meta( predecessor )

    return object_meta


def get_file_meta( classification_file ):
    root = ET.parse( classification_file ).getroot()

    file_attributes = {}
    read_attributes_from_element( root, file_attributes )

    img_date = None if root.find('date') is None else root.find('date').text
    img_time = None if root.find('time') is None else root.find('time').text

    folder = None if root.find('folder') is None else root.find('folder').text
    filename = None if root.find('filename') is None else root.find('filename').text

    path = None if root.find('path') is None else root.find('path').text

    size = root.find('size')
    width, height, depth = int(size.find('width').text), int(size.find('height').text), int(size.find('depth').text)

    item = 0
    labeled_objects = []
    for member in root.findall('object'):
        labeled_objects.append( get_object_meta( member, item=item ) )
        item = item + 1

    return {
        "date": img_date,
        "time": img_time,
        "folder": folder,
        "filename": filename,
        "path": path,
        "size": ( width, height, depth ),
        "objects": labeled_objects,
        "attributes": file_attributes
    }


def put_object_meta( objectE, object_meta ):
    try:

        ET.SubElement( objectE, 'name' ).text = object_meta["name"]

        if 'score' in object_meta and object_meta["score"] is not None:
            ET.SubElement( objectE, 'score' ).text = str( object_meta["score"] )

        # create elements
        bndboxE = ET.SubElement( objectE, 'bndbox' )

        xmin, ymin, xmax, ymax = object_meta["box"]

        ET.SubElement( bndboxE, 'xmin' ).text = str( xmin )
        ET.SubElement( bndboxE, 'ymin' ).text = str( ymin )
        ET.SubElement( bndboxE, 'xmax' ).text = str( xmax )
        ET.SubElement( bndboxE, 'ymax' ).text = str( ymax )

        if "attributes" in object_meta:
            write_attributes_to_element( objectE, object_meta["attributes"])

        if 'predecessor' in object_meta and object_meta["predecessor"] is not None:
            put_object_meta( ET.SubElement( objectE, 'predecessor' ), object_meta["predecessor"] )


    except Exception as e:
        print( "BAD_OBJECT_META: {}\n {}".format( object_meta, e ) )
        raise e
"""

    write a new classification file from meta-data
"""
def put_file_meta( classification_file, meta_data ):
    root = ET.Element( 'annotation' )

    for f in [ 'date', 'time', 'folder', 'filename', 'path' ]:
        if f in meta_data:
            ET.SubElement( root, f ).text = meta_data[f]

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
        put_object_meta( ET.SubElement( root, 'object' ), item )

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

    _, img_time = meta_data['date'], meta_data['time']

    event_timestamp = timetext() if img_time is None else img_time

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



def get_iou(bb1, bb2):
    """
    Calculate the Intersection over Union (IoU) of two bounding boxes.

    Parameters
    ----------
    bb1 : dict
        Keys: {'x1', 'x2', 'y1', 'y2'}
        The (x1, y1) position is at the top left corner,
        the (x2, y2) position is at the bottom right corner
    bb2 : dict
        Keys: {'x1', 'x2', 'y1', 'y2'}
        The (x, y) position is at the top left corner,
        the (x2, y2) position is at the bottom right corner

    Returns
    -------
    float
        in [0, 1]
    """
    assert bb1[0] < bb1[2]
    assert bb1[1] < bb1[3]
    assert bb2[0] < bb2[2]
    assert bb2[1] < bb2[3]

    # determine the coordinates of the intersection rectangle
    x_left = max(bb1[0], bb2[0])
    y_top = max(bb1[1], bb2[1])
    x_right = min(bb1[2], bb2[2])
    y_bottom = min(bb1[3], bb2[3])

    if x_right < x_left or y_bottom < y_top:
        return 0.0

    # The intersection of two axis-aligned bounding boxes is always an
    # axis-aligned bounding box
    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    # compute the area of both AABBs
    bb1_area = (bb1[2] - bb1[0]) * (bb1[3] - bb1[1])
    bb2_area = (bb2[2] - bb2[0]) * (bb2[3] - bb2[1])

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
    assert iou >= 0.0
    assert iou <= 1.0
    return iou



"""

    link up any box predecessors
"""
def connect_predecessors( new_meta, old_meta, min_iou=0.9, min_glitch_score=0.1, min_untruth_score=0.5 ):

    # copy of previous objects
    old_objects = [
        oo
        for oo in old_meta["objects"]
        if oo["score"] >= min_glitch_score
    ]

    for new_object in new_meta["objects"]:

        class_matches = [ oo for oo in old_objects if oo["name"] == new_object["name"] ]

        for k in [ 'predecessor' ]:
            if k in new_object:
                del new_object[k]

        for k in [ 'box-score', 'cardinality', 'iou' ]:
            if k in new_object['attributes']:
                del new_object['attributes'][k]

        if len( class_matches ) == 0:
            continue

        new_object_box = new_object['box']

        ious = [
            ( oo, get_iou( new_object_box, oo['box'] ) )
            for oo in class_matches
        ]

        overlapping_objects = [ oo for oo in ious if oo[1] >= min_iou ]


        if len( overlapping_objects ) == 0:
            continue


        # pick highest scoring
        # TODO: losing information from dupicate boxes
        candidate = max( overlapping_objects, key=lambda oo: oo[0]["score"] )

        old_object = candidate[ 0 ]
        new_object['predecessor'] = old_object

        new_object['attributes']['iou'] = candidate[ 1 ]

        c = 1
        avg_iou = candidate[ 1 ]
        pp = old_object
        while 'predecessor' in pp:
            pp = pp['predecessor']
            c = c + 1
            avg_iou = ( ( avg_iou * ( c - 1 ) ) + get_iou( new_object_box, pp['box'] ) ) / c

        new_object['attributes']['cardinality'] = c
        new_object['attributes']['box-score'] = avg_iou

        old_objects.remove( old_object )
