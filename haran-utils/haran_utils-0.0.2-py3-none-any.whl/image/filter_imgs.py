'''
Moves images from source to target_dir if they have a greater resolution than specified
Positional arguments:
    source_dir
    target_dir
'''
from PIL import Image
import os, shutil

def filter_imgs(args):
    img_dir = args.img_dir
    out_dir = args.out_dir
    dim = args.dim
    total = 0
    success = 0

    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    for img_path in os.listdir(img_dir):
        total +=1
        img_path = os.path.join(img_dir, img_path)
        im = Image.open(img_path)
        if min(im.size) > dim:
            success +=1
            print(f"{img_path}:{im.size} -> {out_dir}")
            shutil.move(img_path, out_dir)
        
        
    print(f"Moved {success} out of {total} images")

