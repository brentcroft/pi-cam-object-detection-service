"""


"""
import math      
"""


"""
def box_area( box=None ):
    return ( box[2] - box[0] ) * ( box[3] - box[1] )
"""


"""
def box_overlap_area( box1, box2 ):
    x_overlap, y_overlap = (
        max( 0, min( box1[2], box2[2] ) - max( box1[0], box2[0] ) ),
        max( 0, min( box1[3], box2[3] ) - max( box1[1], box2[1] ) )
    )
    return x_overlap * y_overlap
"""


"""
def box_overlap_areas( box1, box2 ):
    return [
        box_area( box1 ),
        box_area( box2 ),
        rect_overlap_area( box1, box2 )
    ]
"""


"""
def get_min_max( boxes=None, source_scale=None ):
    width, height = source_scale
    
    if len( boxes ) == 0:
        coords = [ 0, 0, width, height ]
    else:
        coords = [ width, height, 0, 0 ]
        for box in boxes:
            coords = [
                min( coords[0], box[0] ),
                min( coords[1], box[1] ),
                max( coords[2], box[2] ),
                max( coords[3], box[3] )
            ]
    return coords
"""


"""
def get_box_centre( box ):
    return ( 
        int( box[0] + ( float( box[2] - box[0] ) / 2 ) ), 
        int( box[1] + ( float( box[3] - box[1] ) / 2 ) )
    )
"""


"""
def distance( a, b ):
   return math.sqrt( ( a[0] - b[0] )**2 + ( a[1] - b[1] )**2 )
"""


"""
def box_move( box=None, displacement=None, subtract=False, max_size=None  ):
    x_shift, y_shift = ( 
        displacement[0], 
        displacement[1]
    )
    
    if subtract:
        x_shift = -1 * x_shift
        y_shift = -1 * y_shift
    
    box[0] += x_shift
    box[1] += y_shift
    box[2] += x_shift
    box[3] += y_shift
    
    if max_size is not None:
        box_constrain( box=box, max_size=max_size )   

def boxes_move( boxes=None, displacement=None, subtract=False, max_size=None  ):
    for box in boxes:
        box_move( 
            box = box, 
            displacement = displacement, 
            subtract = subtract,
            max_size = max_size
        )
"""


"""
def box_centre_move( box=None, centre=None, step=1, max_size=None ):

    cc = get_box_centre( box )
    
    x_shift, y_shift = ( 
        int( float( centre[0] - cc[0] ) / step ), 
        int( float( centre[1] - cc[1] ) / step ) 
    )
    
    box[0] += x_shift
    box[1] += y_shift
    box[2] += x_shift
    box[3] += y_shift
    
    if max_size is not None:
        box_constrain( box=box, max_size=max_size )
"""


"""
def box_constrain( box=None, max_size=None ):
    cx1, cy1, cx2, cy2 = box
    width, height = max_size        
        
    if cx1 < 0:
        cx2 = min( cx2 - cx1, width )
        cx1 = 0

    if cx2 > width:
        cx1 = max( cx1 - ( cx2 - width ), 0 )
        cx2 = width            
        
    if cy1 < 0:
        cy2 = min( cy2 - cy1, height )
        cy1 = 0
        
    if cy2 > height:
        cy1 = max( cy1 - ( cy2 - height ), 0 )
        cy2 = height
    
    box[0], box[1], box[2], box[3] = int(cx1), int(cy1), int(cx2), int(cy2)
    
