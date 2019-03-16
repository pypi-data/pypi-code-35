import os, sys
def findsub(extension="*", location=(os.getcwd()), keepExtension=True, preserveFilePath=True):
    if extension == "":
        raise TypeError('Extension may not be equal to ""')
    found = []
    len_location = len(location)
    len_extension = len(extension)
    for path, subdirs, files in os.walk(location):
        if preserveFilePath:
            pass

        else:


            if extension == "*":

                if keepExtension:
                    for name in files:
                        filename = os.fsdecode(os.path.join(path, name))
                        _extension = os.path.splitext(filename)[1]
                        join = os.path.join(path, name)[len_location+1:-len(_extension)]
                        if join != '':
                            found.append(filename[len_location+1:])
                else:
                    for name in files:
                        filename = os.fsdecode(os.path.join(path, name))
                        _extension = os.path.splitext(filename)[1]
                        join = os.path.join(path, name)[len_location+1:-len(_extension)]
                        if join != '':
                            found.append(join)


            else:

                if keepExtension:
                    for name in files:
                        filename = os.fsdecode(os.path.join(path, name))
                        if filename.endswith(extension):
                            found.append(os.path.join(path, name)[len_location+1:])
                        else:
                            continue
                else:
                    for name in files:
                        filename = os.fsdecode(os.path.join(path, name))
                        if filename.endswith(extension):
                            found.append(os.path.join(path, name)[len_location+1:-len_extension])
                        else:
                            continue


    return found


    # found = []
    # for file in os.listdir(location):
    #     filename = os.fsdecode(file)
    #     if extension != "*":
    #         if filename.endswith(extension):
    #             found.append(str(filename[:-len(extension)]))
    #         else:
    #             continue
    #     else:
    #         if os.path.isdir(os.path.join(location, file)) == False:
    #             found.append(filename)
    # return found
