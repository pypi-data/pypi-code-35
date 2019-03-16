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
                raise Exception('docmaker not availeble try again later %s' % str(x)) from x
    docmaker = input('do you want to make a doc about a module or a package(typ: module or package):
')
    if docmaker.lower() == 'module':
        path = input('module:
')
        if v:
            print('working...')
        try:
            doc.doc_maker.make_doc(path)
        except Exception as ex:
            if v:
                raise Exception('a error was found msg: %s' % str(ex)) from ex
            else:
                print('error try -v or --verbose for more data')
        else:
            if v:
                print('done!')
    elif docmaker.lower() == 'package':
        path = input('path to package folder:
')
        if v:
            print('working...')
        try:
            doc.helper.HTMLdoc(path)
        except Exception as ex:
            if v:
                raise Exception('a error was found msg: %s' % str(ex)) from ex
            else:
                print('error try -v or --verbose for more data')
        else:
            if v:
                print('done!')
        
    else:
        class ArgumentError(Exception):
            '''argument error'''
        raise ArgumentError('expected input module or package get input: %s' % docmaker)
import sys
def get_commands(args):
    if len(args) < 3:
        return
    ret = {}
    start = 2
    while start < len(args) - 1:
        ret[str(str(str(args[start]).replace('-', '', 1)).replace('--', '', 1))] = args[int(start + 1)]
        start +=2
    return ret

def main(args=None):
    help_msg = 'help for os_sys:
\
commands:
\
    make_doc
\
    help
\
help:
\
    make_doc:
\
        auto doc maker. generates a doc about a package or a module.
\
    help:
\
        shows this help screen
\
using:
\
    os_sys #your-command #your-options
\
example:
\
    os_sys make_doc --verbose'
    """The main routine."""
    if args is None:
        args = sys.argv[1:]
    nargs = args[1:]
    arg = args[0]
    verbose = False
    try:
        for i in nargs:
            if i == '-v' or i == '--verbose':
                verbose = True
    except:
        pass
    if 'make_doc' == arg:
        make_doc(verbose)
    elif 'help' == arg:
        print(help_msg)
    else:
        print(help_msg)
        print('

')
        print('error:', file=sys.stderr)
        print('    command %s is not a os_sys command' % args[0])
if __name__ == "__main__":
    main()
        

