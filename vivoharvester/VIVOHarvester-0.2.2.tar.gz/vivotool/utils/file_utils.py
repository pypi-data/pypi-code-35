import os
import logging
import shutil

from os import path


class Utils:
    """docstring for Utils"""

    def save_photo_file(self, content, filename):

        try:
            file = open(filename, "wb")
            for block in content.iter_content(1024):
                file.write(block)
            file.close()
        except Exception:
            logging.exception("")

    def read_file(self, filename):

        rdfcontent = ""
        try:
            with open(filename, "r") as file:
                rdfcontent = file.read()
        except Exception:
            logging.exception("")

        return rdfcontent

    def save_xml_file(self, content, filename):

        try:
            with open(filename, "w") as file:
                file.write(content)
        except Exception:
            logging.exception("")

    def listfiles(self, path, extension):

        all_files = list(
            filter(
                lambda x: x.endswith(extension),
                os.listdir(path)))

        return sorted(all_files)

    def listdeletefiles(self, path, pattern):

        all_files = list(
            filter(
                lambda x: x.startswith(pattern),
                os.listdir(path)))

        return sorted(all_files)

    def segmentlist(self, inputlist, length):

        result = []
        result = [inputlist[x:x + length]
                  for x in range(0, len(inputlist), length)]

        return result

    def mergefiles(self, folderpath, inputlist, mergefilename):

        with open(path.join(folderpath, mergefilename), 'wb') as wfd:
            for f in inputlist:
                with open(path.join(folderpath, f), 'rb') as fd:
                    shutil.copyfileobj(fd, wfd, 1024 * 1024 * 10)

        return mergefilename
