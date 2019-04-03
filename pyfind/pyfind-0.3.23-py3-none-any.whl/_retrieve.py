import os, sys
def retrieve(location=(os.getcwd()), extension="*", keepExtension=False):
    # """Function that finds files.
    #
    # If ran without parameters,
    #
    # Args:
    #     location: The path to the folder to look inside.
    #         Will not search sub-folders.
    #         Defaults to the cwd of your chosen project
    #     extension: The file extension to look for, use wildcard (*) for any.
    #         Defaults to *
    #     keepExtension: Boolean variable, sets if the return values should
    #         keep the file extensions when added to an array.
    #         Defaults to false
    # Returns:
    #     list: Lists all the resultant files found, with or without
    #         extensions, with regards to the arguments given.
    # """
    if extension == "":
        raise TypeError('Extension may not be equal to ""')
    found = []
    for file in os.listdir(location):
        filename = os.fsdecode(file)
        if extension != "*":
            if filename.endswith(extension):
                found.append(str(filename[:-len(extension)]))
            else:
                continue
        else:
            if os.path.isdir(os.path.join(location, file)) == False:
                found.append(filename)
    return found
