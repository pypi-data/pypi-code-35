import os, argparse, shutil
from ..const import EXAMPLES_FOLDER

parser = argparse.ArgumentParser()
parser.add_argument("name", help="name of the project to create, will be used as folder name")
#parser.add_argument("-u", "--user", help="delete folder if it already exists", action="store_true")

class CreateProject:
    parser = parser

    def run(self, name):
        print('create project', name)
        template_new = os.path.join(EXAMPLES_FOLDER, 'new_project')
        shutil.copytree(template_new, name)
