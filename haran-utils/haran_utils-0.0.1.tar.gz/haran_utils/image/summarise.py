import os
from PIL import Image

def summarise(args):
    print(f"Summary of images")
    dir = args.dir
    depth = args.depth
    for root,dirs,files in os.walk(dir):
        if len(root.split(os.sep)) > 1+depth:
            break
        shapes = {}
        for item in files:
            item_path = os.path.join(root,item)
            if os.path.isfile(item_path):
                try:
                    shape = Image.open(item_path).size
                except OSError:
                    pass
                else:
                    if shape not in shapes.keys():
                        shapes[shape] = 1
                    else:
                        shapes[shape] +=1
        if shapes == {}:
            #print("No images found")
            pass
        else:
            print(root)
            print(shapes)
            print(f"{'-'*10}")
    