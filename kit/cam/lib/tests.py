from os import remove
"""



"""
from ground_truth import put_csv_meta

header = 'folder, filename, width, height, item, name, xmin, ymin, xmax, ymax, score'
body1 = [ 'folder1', 'file1', '101', '201', 'yellow', '11', '21', '31', '41', '0.73498' ]
body2 = [ 'folder2', 'file2', '102', '202', 'green', '12', '22', '32', '42', '0.234' ]

def get_meta_data( body ):
    return {
        'folder': body[0],
        'filename': body[1],
        'size': [ int( body[2] ), int( body[3] ), 3 ],
        'objects': [
            {
                'name': body[4],
                'box': [ int( body[5] ), int( body[6] ), int( body[7] ), int( body[8] ) ],
                'score': float( body[9] )
            }
        ]
    }
csv_log_file = 'test.csv'
try:
    put_csv_meta( csv_file=csv_log_file, meta_data=get_meta_data( body1 ) )
    put_csv_meta( csv_file=csv_log_file, meta_data=get_meta_data( body2 ) )
    
    with open (csv_log_file, "r") as f:
        data=f.readlines()
        
    #print( "data[0]: {}".format( data[0] )) 
    #print( "data[1]: {}".format( data[1] )) 
    
    assert data[0] == "{}\n".format( header )
    assert data[1] == "{}\n".format( ", ".join( body1 ) )
    assert data[2] == "{}\n".format( ", ".join( body2 ) )  
    
except Exception as e:
    raise AssertionError( "{}".format( e ) )
finally:
    remove( csv_log_file )
"""



"""
from storage import get_font


try:
    truetype_font = "DejaVuSansMono.ttf"
    font_size = 12
    config = { "FONT_NAME": truetype_font, "FONT_SIZE": font_size }
    for i in range( 10 ):
        get_font( config )
except Exception as e:
    raise AssertionError( "{}".format( e ) )

    
try:
    truetype_font = "no such font file"
    font_size = 12
    config = { "FONT_NAME": truetype_font, "FONT_SIZE": font_size }
    get_font( config )
    
    raise AssertionError( "Expected exception" )
    
except Exception as e:
    message = "{}".format( e )
    assert message.startswith( "Font not available" )
    assert truetype_font in message
    assert str( font_size ) in message

"""



"""
from util import timestamp, datestamp

print( "timestamp={}".format( timestamp() ) )
print( "datestamp={}".format( datestamp() ) )
"""

"""
from util import calculate_color

# only default color
assert "#ffffff" == calculate_color( "DETECTION FRAME" )

# calculated colors
assert "#154d1c" == calculate_color( "" )

assert "#341f18" == calculate_color( "Watering Can" )
assert "#583c46" == calculate_color( "Exit" )
assert "#1e615e" == calculate_color( "123456" )
assert "#5b6471" == calculate_color( "654321" )

# same values
assert "#341f18" == calculate_color( "Watering Can" )
assert "#583c46" == calculate_color( "Exit" )
assert "#1e615e" == calculate_color( "123456" )
assert "#5b6471" == calculate_color( "654321" )
"""

"""
from util import complementary_color

# as expected
assert "#ffffff" == complementary_color( "#000000" )
assert "#000000" == complementary_color( "#ffffff" )

# but not perfect
assert "#7f7f7f" == complementary_color( "#808080" )
assert "#808080" == complementary_color( "#7f7f7f" )

assert "#cb4515" == complementary_color( "#34baea" )
assert "#34baea" == complementary_color( "#cb4515" )

assert "#a31b31" == complementary_color( "#5ce4ce" )
assert "#5ce4ce" == complementary_color( "#a31b31" )

assert "#a917bd" == complementary_color( "#56e842" )
assert "#56e842" == complementary_color( "#a917bd" )

assert "#8db355" == complementary_color( "#724caa" )
assert "#724caa" == complementary_color( "#8db355" )



