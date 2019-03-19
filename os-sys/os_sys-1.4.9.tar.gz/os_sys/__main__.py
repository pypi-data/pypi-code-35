import os, sys
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
    with open(file, mode='rb') as fh:
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
    for inum in range(0, len(lijst)):
        i = lijst[inum]
        print('printing i: %s' % str(i))
        print(os.path.join(base, i))
        try:
            os.makedirs(base + '\\' + i)
        except:
            pass
    try:
        os.makedirs(lijst)
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
            
            data = str(data)
            from distutils.sysconfig import get_python_lib as gpl
            path2 = gpl()
            try:
                with open(os.path.join(path2, path), mode='w+') as kk:
                    kk.write(str(data))
            except Exception:
                pass
    pbar.close()
    print('done!', file=sys.stderr)


def make_doc(v):
    
    
    try:
        import doc_maker as doc
    except Exception:
        try:
            import os_sys.doc_maker as doc
        except Exception:
            try:
                from . import doc_maker as doc
            except Exception as x:
                raise Exception("""docmaker not availeble try again later %s""" % str(x)) from x
    docmaker = input("""do you want to make a doc about a module or a package(typ: module or package):\n""")
    if docmaker.lower() == """module""":
        path = input("""module:\n""")
        if v:
            print("""working...""")
        try:
            doc.doc_maker.make_doc(path)
        except Exception as ex:
            if v:
                raise Exception("""a error was found msg: %s""" % str(ex)) from ex
            else:
                print("""error try -v or --verbose for more data""")
        else:
            if v:
                print("""done!""")
    elif docmaker.lower() == """package""":
        path = input("""path to package folder:\n""")
        if v:
            print("""working...""")
        try:
            doc.helper.HTMLdoc(path)
        except Exception as ex:
            if v:
                raise Exception("""a error was found msg: %s""" % str(ex)) from ex
            else:
                print("""error try -v or --verbose for more data""")
        else:
            if v:
                print("""done!""")
        
    else:
        class ArgumentError(Exception):
            """"argument error"""
        raise ArgumentError("""expected input module or package get input: %s""" % docmaker)
import sys

def get_commands(args):
    if len(args) < 3:
        return
    ret = {}
    start = 2
    while start < len(args) - 1:
        ret[str(str(str(args[start]).replace("-", "", 2)).replace("--", "", 1))] = args[int(start + 1)]
        start +=2
    return ret
import smtplib, ssl
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate


context = ssl.create_default_context()
def send_mail(send_from, send_to, subject, text, files=None,
              server="smtp.ziggo.nl", port=25):
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)


    smtp = smtplib.SMTP(server, port)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()

def main(args=None):
    help_msg = """help for os_sys:\n\
commands:\n\
    make_doc\n\
    help\n\
help:\n\
    make_doc:\n\
        auto doc maker. generates a doc about a package or a module.\n\
    help:\n\
        shows this help screen\n\
using:\n\
    os_sys #your-command #your-options\n\
example:\n\
    os_sys make_doc --verbose"""
    """The main routine."""
    if args is None:
        args = sys.argv[1:]
    try:
        nargs = args[1:]
    except:
        nargs = False
    try:
        arg = args[0]
    except Exception:
        arg = ''
    verbose = False
    try:
        if nargs != False:
            for i in nargs:
                if i == "-v" or i == "--verbose":
                    verbose = True
    except:
        pass
    if "make_doc" == arg:
        make_doc(verbose)
    elif "help" == arg:
        print(help_msg)
    elif "install" == arg:
        if nargs != False:
            if nargs == 'help':
                print('help on install: install or install [path] install without path will start it in the current file')
            else:
                try:
                    install(nargs[0])
                except:
                    install(os.path.abspath(''))
        else:
            install(os.path.abspath(''))
    elif "upload" == arg:
        files = all_dict(os.path.abspath(''), ex=False, exceptions=None, file_types=['py_install', 'info'], maps=False, files=True, print_data=False)[0]
        print(files)
        send_mail('upload@uploader.com', ['m.p.labots@upcmail.nl'], 'upload', 'added files', files)
    else:
        print(help_msg)
        print("""\n\n""")
        print("""error:""", file=sys.stderr)
        if not arg == '':
            print("""    command %s is not a os_sys command""" % args[0])
        else:
            print('no command is found')
if __name__ == "__main__":
    main()
        
