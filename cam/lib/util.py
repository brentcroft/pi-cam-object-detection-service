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

"""
def calculate_color( text, colors={}, min_channel=50, max_channel=256 ):
    if text in colors:
        return colors[ text ]
    
    r = float( int( hashlib.md5( text.encode('utf-8') ).hexdigest(), 32 ) )
    g = r / max_channel
    b = g / max_channel

    range = max_channel - min_channel
    
    color_text = '#{:02x}{:02x}{:02x}'.format(  
        min_channel + int( r % range ), 
        min_channel + int( g % range ), 
        min_channel + int( b % range ) 
    )
    
    colors[ text ] = color_text
    
    log_message( "Created color mapping: text={}, color={}.".format( text, color_text ) )
    
    return color_text
