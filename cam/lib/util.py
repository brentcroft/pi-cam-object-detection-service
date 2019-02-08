import os
import sys
import time
import datetime

current_milli_time = lambda: int(round(time.time() * 1000))
  
def timestamp():
    now = time.time()
    localtime = time.localtime(now)
    milliseconds = '%03d' % int((now - int(now)) * 1000)
    return time.strftime('%H-%M-%S_', localtime) + milliseconds
   
def datestamp():
    return str( datetime.date.today() )    

def log_message( message ):
    time.ctime()
    print( '[{}] {}'.format( timestamp(), message ) )
    sys.stdout.flush()

def switch_file( source, target ):
    if os.path.isfile( target ):
        os.remove( target )
    os.rename( source, target )  
