'''
Script to center crop and resize images
Positional Args:
    output_dir: Dir to which the images would be output
    Any number of input images
'''
import os
from PIL import Image
import time
def crop(args):
    in_dir = args.in_dir
    out_dir = args.out_dir
    image_size = args.dim.split(',')
    image_size = (int(image_size[0]),int(image_size[1])) 
    img_paths = os.listdir(in_dir)
    total = len(img_paths)
    i = 0
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    for img_path in img_paths:
        i +=1
        out_path = os.path.join(out_dir, os.path.split(img_path)[-1])
        img_full_path = os.path.join(in_dir, img_path)
        im = Image.open(img_full_path)
        # sys.stdout.write(f"\r{img_full_path}:{im.size} -> {out_path}:{image_size} {i}/{total}")
        # sys.stdout.flush()
        print(f"{i}/{total} {img_full_path}:{im.size} -> {out_path}:{image_size}\t")

        w, h = im.size
        min_dim = min(w,h)
        left = w/2 - min_dim/2
        right = w/2 + min_dim/2
        upper = h/2 - min_dim/2
        lower = h/2 + min_dim/2
        im = im.crop((left,upper,right, lower))
        im.thumbnail(image_size)
        im.save(out_path)