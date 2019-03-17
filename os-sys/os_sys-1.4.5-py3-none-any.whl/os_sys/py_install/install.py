#installer
#python3.7
#devlopment
import os, sys
__all__ = ['install']
import tqdm
def all_dict(dictory, ex=False, exceptions=None, file_types=['py_install'], maps=False, files=True, print_data=False):
    import os
    data = []
    string_data = ''
    e = exceptions
    if 'list' in str(type(e)) or e == None:
        pass
    else:
        raise TypeError('expected a list but got a %s' % type(e))
    e = file_types
    if 'list' in str(type(e)) or e == None:
        pass
    else:
        raise TypeError('expected a list but got a %s' % type(e))
    
    print_ = True if print_data == 'print' or print or True else False
    
    for dirname, dirnames, filenames in os.walk(dictory):
        # print path to all subdirectories first.
        if maps:
            for subdirname in dirnames:
                dat = os.path.join(dirname, subdirname)
                data.append(dat)
                string_data = string_data + '\n' + dat
                if print_:
                    print(dat)

        # print path to all filenames.
        if files:
            for filename in filenames:
                s = False
                fname_path = filename
                file = fname_path.split('.')
                no = int(len(file) - 1)
                file_type = file[no]
                if not e == None:
                    for b in range(0, len(e)):
                        if e[b] == file_type:
                            s = True
                            
                if e == None:
                    s = True
                if s:
                    s = False   
                            
                    dat = os.path.join(dirname, filename)
                    data.append(dat)
                    string_data = string_data + '\n' + dat
                    if print_:
                        
                        print(dat)
        
        

        # Advanced usage:
        # editing the 'dirnames' list will stop os.walk() from recursing into there.
        if not exceptions == None:
            
            for ip in range(0, int(len(exceptions))):
                exception = exceptions[ip]
                
                if exception in dirnames:
                    # don't go into any .git directories.
                    dirnames.remove(exception)
                elif exception in filename and data:
                    data.remove(exception)
        if len(dirnames) == 1 and ex:
            break
    
    return [data, string_data]
def stl(s):
    # string naar lijst
    l = []
    for i in range(0,len(s)): l += s[i]
    return l
def install(path):
    global name
    print('searching files...', file=sys.stderr)
    file = all_dict(path)[0][0]
    from distutils.sysconfig import get_python_lib as gpl
    print('building...', file=sys.stderr)
    with open(file) as fh:
        mystr = str(fh.read())
    with open(all_dict(path, ex=False, exceptions=None, file_types=['info'], maps=False, files=True, print_data=False)[0][0]) as info:
        rpackage_info = str(info.read())
    package_info = rpackage_info.split('\n')
    print('getting info about package...', file=sys.stderr)
    info_dict = {}
    for small in package_info:
        try:
            key, value = small.split('=')
            info_dict[key] = value
            value = value
            
        except:
            pass
        else:
            if 'name' in key:
                from distutils.sysconfig import get_python_lib as gpl
                base_path = os.path.join(gpl(), value)
                name = value
                del key, value
                continue
            elif key == 'version':
                version = value
                del key, value
                continue
            else:
                del key, value
                continue
    from distutils.sysconfig import get_python_lib as gpl
    print('generating info file...', file=sys.stderr)
    lijst = info_dict['maps']
    lijst = str(str(str(str(lijst.replace('[', '')).replace(']', '')).replace("'", '')).replace('\\\\', '\\')).split(", ")
    print(type(lijst))
    
    base = gpl() + '\\' + info_dict['name']
    try:
        os.removedirs(base)
    except Exception:
        pass
    try:
        os.mkdir(base)
    except Exception:
        pass
    print(lijst)
    for inum in range(0, len(lijst)):
        i = lijst[inum]
        print('printing i: %s' % str(i))
        print(os.path.join(base, i))
        try:
            os.mkdir(base + '\\' + i)
        except:
            pass
    with open(os.path.join(gpl(), info_dict['name'], 'data.info'), mode='w+') as done:
        done.write(rpackage_info)
    print('unzipping...', file=sys.stderr)
    mystr = mystr.split('##########')
    print('installing...', file=sys.stderr)
    import time
    pbar = tqdm.tqdm(mystr)
    for i in pbar:
        
        try:
            path, data = i.split('>>>>>>>>>>>>>>>')
            a = path
        except Exception:
            pass
        else:
            pbar.set_description(r" Processing %s" % a)
            data = str(data)
            from distutils.sysconfig import get_python_lib as gpl
            path2 = gpl()
            try:
                with open(os.path.join(path2, path), mode='w+') as kk:
                    kk.write(str(data))
            except Exception:
                pass
    print('done!', file=sys.stderr)
install(os.path.abspath(''))
