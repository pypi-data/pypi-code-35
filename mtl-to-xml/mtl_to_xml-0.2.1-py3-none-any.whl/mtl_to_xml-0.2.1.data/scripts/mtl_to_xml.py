#!python
# Convert Landsat MTL text files to .xml using standard ElementTree
# Python 3.7

import os
import argparse
import fileinput
import xml.etree.ElementTree as etree


def target_mode(file_name):
    # send a single file to the mtl_to_xml conversion
    mtl_to_xml(file_name)


def scan_mode():
    # walk current directory and sub directories. scan each directory for MTL files and convert them.
    pwd = os.getcwd()
    for root, subfolders, files in os.walk(pwd):
        scan_dir(root)


def scan_dir(pwd):
    # Builds a dictionary of filepath:filename of all MTL files in a directory
    # Sends that dictionary to mtl_to_xml for conversion

    dir_file_list = os.listdir(pwd)  # get list of all files in present working directory
    mtl_dict = {}                    # dict to hold filepath:filename

    print('Searching in:', pwd)

    for file_name in dir_file_list:  # locate MTL files and place them in our working list
        if '_MTL.txt' in file_name:
            print('Found:', file_name)
            mtl_dict[pwd+'/'+file_name] = file_name

    mtl_to_xml(mtl_dict)


def mtl_to_xml(mtl_dict):
    # converts mtl to xml
    for key in mtl_dict:
        new_file = key.replace('.txt', '.xml')   # new .xml file to be created
        try:
            with fileinput.input(files=key, mode='r') as f:  # fileinput is used instead of open so we can readline()
                first_line = f.readline().strip()
                first_line = first_line[(first_line.index('=')) + 2:]
                root = etree.Element(first_line)                               # capture first line as root Element
                current_group = ''                                             # temp var for storing current Element

                for line in f:
                    try:
                        temp = line.strip()                         # remove unneeded whitespace
                        temp = temp.replace("\"", "")               # remove unneeded double quotes
                        pre = temp[0:temp.index('=') - 1]           # getting a "key" for xml
                        post = temp[temp.index('=') + 2:]           # getting a "value" for xml
                    except Exception as e:
                        break                                       # when we hit the end of the file, silently break
                    if pre == 'END_GROUP':
                        continue
                    elif pre == 'GROUP' in line:                    # in the mtl file, groups are children of root
                        current_group = post
                        etree.SubElement(root, current_group)
                    elif '=' in line:
                        temp_element = etree.SubElement(root.find(current_group), pre)  # setting a "key" in xml
                        temp_element.text = post                                        # setting a "value" in xml

                for element in root:                                # indent for pretty print
                    indent(element)

                xml_tree = etree.ElementTree(root)
                xml_tree.write(new_file, encoding="us-ascii", xml_declaration=True)
        except FileNotFoundError:
            print('That file does not exist.')
        except Exception as e:
            print('Something went wrong.')
            print(e)


def indent(elem, level=0):
    # https://effbot.org/zone/element-lib.htm#prettyprint
    # indent method from Fredrik Lundh

    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def main():

    parser = argparse.ArgumentParser(
        description='Choose target \'-t\', directory \'-d\', or scan \'-s\'mode to convert Landsat MTL to XML.')

    parser.add_argument('-t', '--target',
                        action='store',
                        required=False,
                        help='Target mode converts a single MTL file to XML. \n '
                        'The script must be run in the same directory as the MTL file. \n '
                        'Example: mtl_to_xml -t your_landsat_file_MTL.txt \n')

    parser.add_argument('-d', '--directory',
                        action='store_const',
                        const='-d',
                        required=False,
                        help='Directory mode converts all MTL files in the current directory to XML. \n'
                        'The script must be run in the same directory as the MTL files. \n'
                        'Example: mtl_to_xml -d \n')

    parser.add_argument('-s', '--scan',
                        required=False,
                        action='store_const',
                        const='-s',
                        help='Scan mode converts all MTL files in the current directory to XML, '
                        'and then searches all sub-directories '
                        'and converts the MTL files that it finds. \n'
                        'Example: mtl_to_xml -s \n')

    args = parser.parse_args()

    if args.target:
        target_mode(args.target)
    elif args.directory:
        scan_dir(os.getcwd())
    elif args.scan:
        scan_mode()


if __name__ == '__main__':
    main()
