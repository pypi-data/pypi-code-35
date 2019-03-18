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
def install(path):
    try:
        import py_install as py_install
    except Exception:
        try:
            import os_sys.py_install as py_install
        except Exception:
            try:
                from . import py_install as py_install
            except Exception as x:
                raise Exception("""Py_install not availeble try again later %s""" % str(x)) from x
    else:
        py_install.install.install(path)
def get_commands(args):
    if len(args) < 3:
        return
    ret = {}
    start = 2
    while start < len(args) - 1:
        ret[str(str(str(args[start]).replace("-", "", 2)).replace("--", "", 1))] = args[int(start + 1)]
        start +=2
    return ret

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
        arg = args[0]
    except Exception:
        arg = ''
    verbose = False
    try:
        for i in nargs:
            if i == "-v" or i == "--verbose":
                verbose = True
    except:
        pass
    if "make_doc" == arg:
        make_doc(verbose)
    elif "help" == arg:
        print(help_msg)
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
        
