#!python
# Convert Landsat MTL text files to .xml using standard ElementTree.
# Python 3.7

import os
import argparse
import fileinput
import xml.etree.ElementTree as etree


def target_mode(file_name):
    # Send a single file to the mtl_to_xml conversion method.
    mtl_dict = {file_name: file_name}
    mtl_to_xml(mtl_dict)


def scan_mode():
    # Walk current directory and sub directories. Search each directory for MTL files and convert them.
    pwd = os.getcwd()
    for root, subfolders, files in os.walk(pwd):
        scan_dir(root)


def scan_dir(pwd):
    # Builds a dictionary filepath:filename of all MTL files in a directory.
    # Sends that dictionary to the mtl_to_xml conversion method.

    # Get list of all files in present working directory
    dir_file_list = os.listdir(pwd)

    # Dictionary to hold filepath:filename
    mtl_dict = {}

    # Let the user know where the script looked.
    print('Searching in:', pwd)

    # Locate MTL files and place them in a working List
    for file_name in dir_file_list:
        if '_MTL.txt' in file_name:

            # Let the user know which files the script found.
            print('Found:', file_name)

            # Add filepath:filename to the dictionary
            mtl_dict[pwd+'/'+file_name] = file_name

    # Send the Dictionary of filepath:filename to mtl_to_xml conversion method.
    mtl_to_xml(mtl_dict)


def mtl_to_xml(mtl_dict):
    # Converts Landsat MTL metadata file to XML.
    # Output the XML in the same directory as the MTL

    for key in mtl_dict:
        try:
            with fileinput.input(files=key, mode='r') as f:
                # Read first line of MTL as root Element.
                first_line = f.readline().strip()
                # For it's tree-like structure, MTL files are organized in 'Groups = Group_Name_Here'.
                # We want to strip out 'Groups = ' and get only the Group name.
                first_line = first_line[(first_line.index('=')) + 2:]
                # Create the root of the ElementTree from the first Group in the MTL file.
                root = etree.Element(first_line)
                # Holding variable for storing current Element
                current_group = ''

                for line in f:
                    # Remove unneeded whitespace.
                    temp = line.strip()
                    # Remove unneeded double quotes.
                    temp = temp.replace("\"", "")

                    # Silently break when hitting end of MTL file.
                    if temp == 'END':
                        break

                    try:
                        # MTL is structured like a series of key:value pairs separated by an '='.
                        # pre gets the 'key' before the '='
                        # post get the 'value' after the '='
                        pre = temp[0:temp.index('=') - 1]
                        post = temp[temp.index('=') + 2:]
                    except Exception as e:
                        # A catch-all Exception block isn't a good idea.
                        # When we hit the end of the file, silently break.
                        print('Make sure you\'re using an un-edited MTL file.')
                        print(e)
                        break
                    # MTL files use End_Group to denote the end of an Element.
                    # When we hit the end of an element, silently continue.
                    if pre == 'END_GROUP':
                        continue
                    # MTL files use Group to denote the start of an Element.
                    elif pre == 'GROUP' in line:
                        # Add the Group to the ElementTree as a SubElement
                        etree.SubElement(root, post)
                        # This temp variable points to the current MTL Group, and is used in the next elif statement.
                        current_group = post
                    elif '=' in line:
                        # From the root of the ElementTree, find the current_group and establish a new SubElement.
                        # Sets the key in key:value.
                        element = etree.SubElement(root.find(current_group), pre)
                        # Add text to the SubElement. Sets the value in key:value.
                        element.text = post

                # Indent the new XML file for pretty print.
                for element in root:
                    indent(element)

                # New .xml file to be created
                new_file = key.replace('.txt', '.xml')

                # Build an ElementTree from the Elements and SubElements created above.
                xml_tree = etree.ElementTree(root)

                # Write out the ElementTree to the new .xml file.
                xml_tree.write(new_file, encoding="us-ascii", xml_declaration=True)

        except FileNotFoundError:
            print('That file does not exist.')
        except Exception as e:
            print('Something went wrong.')
            print(e)


def indent(elem, level=0):
    # Indent method from Fredrik Lundh
    # https://effbot.org/zone/element-lib.htm#prettyprint

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


def parse_args():
    parser = argparse.ArgumentParser(
        description='Choose target \'-t\', directory \'-d\', or scan \'-s\' mode to convert Landsat MTL to XML.')

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
    return args


def main():

    args = parse_args()

    # Target mode. Converts a single file.
    if args.target:
        target_mode(args.target)
    # Directory mode. Scans one directory for MTL files and converts them to XML.
    elif args.directory:
        scan_dir(os.getcwd())
    # Scans top directory and all subdirectories. Converts the MTL files it finds to XML.
    elif args.scan:
        scan_mode()


if __name__ == '__main__':
    main()
