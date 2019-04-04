import sys
from extract_face import extract_face


image_path = str(input("Specify the path of the image :- "))
if not image_path:
    print("Exception:- Enter path of image")
    sys.exit()
try:
    scale_factor = float(input("Specifying how much the image size is reduced at each image scale (default - 1.1) :- ") or "1.1")
except ValueError as e:
    print("Exception:- Enter correct float value")
    sys.exit()

output_directory = input("Directory where to save output (default - same as input image) :- ") or None
                    
output_prefix = input("Prefix of output (default - the name of input image) :- ") or None

try:
    extract_face(image_path = image_path,
                scale_factor = scale_factor,
                output_directory = output_directory,
                output_prefix = output_prefix)
except Exception as e:
    print("Exception:- " + str(e))
    sys.exit()