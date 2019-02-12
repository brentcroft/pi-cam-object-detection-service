import os
import sys
import time
import datetime
import hashlib

"""

"""
current_milli_time = lambda: int(round(time.time() * 1000))
"""

"""
def timestamp():
    now = time.time()
    localtime = time.localtime(now)
    milliseconds = '%03d' % int((now - int(now)) * 1000)
    return time.strftime('%H-%M-%S_', localtime) + milliseconds
"""

"""
def datestamp():
    return str( datetime.date.today() )    
"""

"""
def log_message( message ):
    time.ctime()
    print( '[{}] {}'.format( timestamp(), message ) )
    sys.stdout.flush()
"""

"""
def switch_file( source, target ):
    if os.path.isfile( target ):
        os.remove( target )
    os.rename( source, target )  
"""

    Specify fixed colors.
    
"""
DEFAULT_COLORS = {
    "DETECTION FRAME": "#ffffff"
}
"""

    Calculate (and cache) an RGB color hex string for any text.
    
    For a given min_channel & max_channel then the same color is returned for any given text.
    
"""
def calculate_color( text, colors=DEFAULT_COLORS, min_channel=20, max_channel=120, no_cache=False ):
    if not no_cache and text in colors:
        return colors[ text ]
    
    # take the first (3x4) hex characters
    hex = hashlib.md5( text.encode('utf-8') ).hexdigest()[0:12]
    
    range = max_channel - min_channel

    r = min_channel + ( int( hex[0:4], 16 ) % range )
    g = min_channel + ( int( hex[4:8], 16 ) % range )
    b = min_channel + ( int( hex[8:12], 16 ) % range )
    
    color_text = '#{:02x}{:02x}{:02x}'.format( r, g, b )
    
    if not no_cache:
        colors[ text ] = color_text    
        log_message( "Created color mapping: text=[{:<15}], hash=[{}], color=[{}], rgb={}".format( text, hex, color_text, (r,g,b) ) )
    
    return color_text
"""

    

""" 
def complementary_color( hex_color, colors={} ):
    if hex_color in colors:
        return colors[ hex_color ]
    
    if hex_color[0] != '#':
        raise ValueError( "Color value does not begin with '#': {}".format( hex_color ) )
    
    # pairs of hex characters after initial hash character
    c = hex_color[1:]        
    rgb = ( c[0:2], c[2:4], c[4:6] )
    comp = [ '{:02x}'.format( 255 - int( a, 16 ) ) for a in rgb ]
    
    color_text = "#{}".format( ''.join( comp ) )
    colors[ hex_color ] = color_text
    
    log_message( "Created color complement: [{} / {}]".format( hex_color, color_text ) )

    return color_text
