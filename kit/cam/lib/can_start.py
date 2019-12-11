"""
    DO NOT IMPORT THIS MODULE
    IT RETURNS EXIT=0
"""
import sys

from cam_config import read_config
from cam_config import get_light_level
from cam_config import get_charge_level

from util import log_message
from still_camera import StillCamera
"""

"""
def check_charge_level( config ):
    try:
        from pijuice import PiJuice
        
        try:
            
            min_charge_start, charge_level = config['MIN_CHARGE_START'], get_charge_level( PiJuice( 1, 0x14 ) )

            if charge_level < min_charge_start:
                log_message( "Insufficient battery charge to start: {}% < {}%".format( charge_level, min_charge_start ) )
                sys.exit( 1 )   

            log_message( "Battery charge acceptable: {}%".format( charge_level ) )        
                
        # don't want to return errors to calling script
        except Exception as e:
            log_message( "Ignoring error checking charge level: {}".format( e ) )
            
    except Exception as e:
        log_message( "No PiJuice" )

def check_light_level( config ):
    try:
        min_light_level = config['MIN_LIGHT_LEVEL']

        camera = StillCamera()
        
        try:
            camera.start()

            light_level = get_light_level( camera.pil_image() )
        
        finally:
            camera.stop()

        if light_level < min_light_level:
            log_message( "Insufficient light to start: {}% < {}%".format( light_level, min_light_level ) )
            sys.exit( 1 )  

        log_message( "Light level acceptable: {}%".format( light_level ) )

    # don't want to return errors to calling script
    except Exception as e:
        log_message( "Ignoring error checking light level: {}".format( e ) )

# 

if __name__ == '__main__':

    config = read_config()
    
    check_charge_level( config )
    
    check_light_level( config )

    sys.exit( 0 )
