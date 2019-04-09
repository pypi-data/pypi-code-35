import argparse
import haran_utils.image.image as image
import sys

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

parser = MyParser(add_help=False, description="Useful utilities. Type -h for help.")    
command_dict = {'image': image.main}
parser.add_argument('command', choices = list(command_dict.keys()))

def main():
    args, sub_args = parser.parse_known_args()
    if args.command in command_dict.keys():
        command_dict[args.command](sub_args)
    else:
        print("Error")

if __name__ == "__main__":
    main()