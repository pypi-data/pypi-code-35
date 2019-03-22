import os


def _get_doc_file(file_path):

    basename = os.path.basename(file_path)
    dir_name = file_path[:-len(basename)]

    path = dir_name+os.sep+".."+os.sep+os.sep+"treep_documentation.txt"
    path = os.path.abspath(path)

    if not os.path.isfile(path):
        raise Exception("failed to find documentation text file in "+path)
    
    return path


def display_documentation(bin_path):

    path = _get_doc_file(bin_path)

    with open(path,"r") as f:
        lines = f.readlines()

    for line in lines:
        print(line.replace('\n',''))

    
