"""
    see:
    https://docs.python.org/3/library/http.server.html#http.server.HTTPServer
"""
import http.server
import socketserver
"""


"""
import os
from shutil import copyfile
from cam_config import read_config
"""


"""
config = read_config()

if 'CURRENT_IMAGE_STORE' not in config:
    raise ValueError( "'CURRENT_IMAGE_STORE' not in config." )

web_dir = config['CURRENT_IMAGE_STORE']

# default is 8080
port = config['CURRENT_IMAGE_PORT'] if 'CURRENT_IMAGE_PORT' in config else 8080
"""


"""
try:    
    # ram directory is empty on restart
    # so ensure site files
    site_dir = "./site"
    for site_file in os.listdir( site_dir ):
        copyfile( os.path.join( site_dir, site_file ), os.path.join( web_dir, site_file ) )
    
    # now change dir so server serves site files
    os.chdir( web_dir )
    
    httpd = socketserver.TCPServer( ( "", port ), http.server.SimpleHTTPRequestHandler )
    httpd.serve_forever()
    
finally:
    if httpd is not None:
        httpd.shutdown()
        httpd = None