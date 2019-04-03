import os, sys
def findsub(extension="*", location=(os.getcwd()), keepExtension=True, preserveFilePath=True):
    if extension == "":
        raise TypeError('Extension may not be equal to ""')
    found = []
    len_location = len(location)
    len_extension = len(extension)
    for path, subdirs, files in os.walk(location):
        if preserveFilePath:
            if extension == "*":
                if keepExtension:
                    for name in files:
                        filename = os.fsdecode(os.path.join(path, name))
                        _extension = os.path.splitext(filename)[1]
                        join = os.path.join(path, name)[:-len(_extension)]
                        if join != '':
                            found.append(filename[:])
                else:
                    for name in files:
                        filename = os.fsdecode(os.path.join(path, name))
                        _extension = os.path.splitext(filename)[1]
                        join = os.path.join(path, name)[:-len(_extension)]
                        if join != '':
                            found.append(join)
            else:
                if keepExtension:
                    for name in files:
                        filename = os.fsdecode(os.path.join(path, name))
                        if filename.endswith(extension):
                            found.append(os.path.join(path, name)[:])
                        else:
                            continue
                else:
                    for name in files:
                        filename = os.fsdecode(os.path.join(path, name))
                        if filename.endswith(extension):
                            found.append(os.path.join(path, name)[:-len_extension])
                        else:
                            continue
        else:
            if extension == "*":
                if keepExtension:
                    for name in files:
                        filename = os.fsdecode(os.path.join(path, name))
                        _extension = os.path.splitext(filename)[1]
                        join = os.path.join(path, name)[:-len(_extension)]
                        if join != '':
                            found.append(filename[:])
                else:
                    for name in files:
                        filename = os.fsdecode(os.path.join(path, name))
                        _extension = os.path.splitext(filename)[1]
                        join = os.path.join(path, name)[:-len(_extension)]
                        if join != '':
                            found.append(join)
            else:
                if keepExtension:
                    for name in files:
                        filename = os.fsdecode(os.path.join(path, name))
                        if filename.endswith(extension):
                            found.append(os.path.join(path, name)[:])
                        else:
                            continue
                else:
                    for name in files:
                        filename = os.fsdecode(os.path.join(path, name))
                        if filename.endswith(extension):
                            found.append(os.path.join(path, name)[:-len_extension])
                        else:
                            continue
    return found
