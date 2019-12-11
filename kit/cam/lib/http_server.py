"""
    see:
    https://docs.python.org/3/library/http.server.html#http.server.HTTPServer
    https://gist.github.com/gnilchee/246474141cbe588eb9fb
"""
import socketserver

import sys, os, socket
from socketserver import ThreadingMixIn, TCPServer
from http.server import SimpleHTTPRequestHandler, HTTPServer

"""


"""
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
def copy_child_items( source_dir, target_dir ):
    # site_dir = "./site"
    for item in os.listdir( source_dir ):
        source_item = os.path.join( source_dir, item )
        target_item = os.path.join( target_dir, item )
        if os.path.isdir( source_item ):
            if not os.path.exists( target_item ):
                os.mkdir( target_item )
            copy_child_items( source_item, target_item )
        else:
            copyfile( source_item, target_item )


class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass


httpd = None

try:
    # ram directory is empty on restart
    # so ensure site files
    copy_child_items( "./site", web_dir )

    # now change dir so server serves site files
    os.chdir( web_dir )

    #httpd = TCPServer( ( "", port ), SimpleHTTPRequestHandler )
    httpd = ThreadingSimpleServer( ( '0.0.0.0', port ), SimpleHTTPRequestHandler )
    
    httpd.serve_forever()

finally:
    if httpd is not None:
        httpd.shutdown()
        httpd = None