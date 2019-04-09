import argparse
from PIL import Image
import os, sys
from haran_utils.image.crop import crop
from haran_utils.image.filter_imgs import filter_imgs
from haran_utils.image.summarise import summarise


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

parser = MyParser()
sub_parsers = parser.add_subparsers(help="Image related scripts")
resl_parser = sub_parsers.add_parser('summarise', help="Prints the number of images per resolution in each subdirectory")
resl_parser.add_argument('dir', type=str)
resl_parser.add_argument('--depth', default=1, type=int)
resl_parser.set_defaults(func=summarise)

crop_parser = sub_parsers.add_parser('crop', help="Resize and crops images")
crop_parser.add_argument('in_dir', type=str, help="Directory containing images to be cropped")
crop_parser.add_argument('out_dir', type=str, help="Directory to which the output images will be saved")
crop_parser.add_argument('--dim', default='256,256', type=str)
crop_parser.set_defaults(func=crop)

filter_parser = sub_parsers.add_parser('filter', help="Moves images greater than the specified resolution to output directory")
filter_parser.add_argument('img_dir', type=str, help="Directory containg images to be filtered")
filter_parser.add_argument('out_dir', type=str, help="Directory to which the filtered images will be saved")
filter_parser.add_argument('dim', type=int, help="Image dimension based on which to filter")
filter_parser.set_defaults(func=filter_imgs)

def main(incoming_args):
    args = parser.parse_args(incoming_args)
    try:
        args.func(args)
    except AttributeError:
        parser.print_help()

# if __name__ == "__main__":
#     main()