
from io import BytesIO
from PIL import Image
import picamera
import datetime as dt

from time import sleep
from fractions import Fraction

from util import log_message

class StillCamera():

    def __init__( 
            self, 
            image_format='jpeg', 
            resolution=( 640, 480 ), 
            rotation=None, 
            name=None, 
            framerate=5, 
            shutter_speed=None, 
            iso=None ):

        self.name = name
        self.resolution = resolution
        self.rotation = rotation
        self.image_format = image_format
        
        self.framerate = framerate
        self.shutter_speed = shutter_speed
        self.iso = iso
        
        self.started = 0
        
    def start(self):
        log_message( 'StillCamera: starting ...')
        
        if self.started == 0:
            
            self.camera = picamera.PiCamera()
            
            self.camera.resolution = self.resolution
            
            if self.rotation is not None:
                self.camera.rotation = self.rotation
            
            if self.name is not  None:
                self.camera.annotate_text = self.name
                
            if self.framerate is not None:
                self.camera.framerate = self.framerate

            if self.shutter_speed is not None:
                self.camera.shutter_speed = self.shutter_speed  

            if self.iso is not None:
                self.camera.iso = self.iso                 
            

            sleep( 10 )                
                
            self.started = 1 
            
            log_message( 'StillCamera: started.')
        else:
            log_message( 'StillCamera: Not stopped!')
            
            
    def pil_image(self):
        if self.started == 1:
            # see: https://picamera.readthedocs.io/en/release-1.13/recipes1.html#capturing-to-a-pil-image
            stream = BytesIO()
            self.camera.capture( stream, self.image_format )
            stream.seek( 0 )
            image = Image.open( stream )
            image.load()
            return image
            
        else:
            raise ValueError( 'StillCamera: Not started!')            
            
        
    def stop(self):
        log_message( 'StillCamera: stopping ...')
        if self.started == 1:
            self.started = 0            
            self.camera.close()
            self.camera = None
            
            log_message( 'StillCamera: stopped.')
        else:
            log_message( 'StillCamera: Not started!')

