import os, sys
def find(extension="*", location=(os.getcwd()), keepExtension=True, preserveFilePath=True):
    """Function that finds files.

    If ran without parameters,

    Args:
        location: The path to the folder to look inside.
            Must be passed in as a raw string, for example r"D:\Users"
            Will not search sub-folders.
            Defaults to the cwd of your chosen project
        extension: The file extension to look for, use wildcard (*) for any.
            Defaults to *
        keepExtension: Boolean variable, sets if the return values should
            keep the file extensions when added to an array.
            Defaults to false
    Returns:
        list: Lists all the resultant files found, with or without
            extensions, with regards to the arguments given.
    """
    if extension == "":
        raise TypeError('Extension may not be equal to ""')
    found = []
    for file in os.listdir(location):
        filename = os.fsdecode(file)
        if extension != "*":
            if filename.endswith(extension):
                if preserveFilePath:
                    if keepExtension:
                        found.append(os.path.join(location, str(filename[:])))
                    else:
                        found.append(os.path.join(location, str(filename[:-len(extension)])))
                else:
                    if keepExtension:
                        found.append(str(filename[:]))
                    else:
                        found.append(str(filename[:-len(extension)]))
            else:
                continue
        else:
            if os.path.isdir(os.path.join(location, file)) == False:
                if preserveFilePath:
                    found.append(os.path.join(location, filename))
                else:
                    found.append(filename)
    return found

# https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory
#
# This will iterate over all descendant files, not just the immediate children of the directory:
#
# import os
#
# for subdir, dirs, files in os.walk(rootdir):
#     for file in files:
#         #print os.path.join(subdir, file)
#         filepath = subdir + os.sep + file
#
#         if filepath.endswith(".asm"):
#             print (filepath)
