from dependencies.docopt import docopt
from lib.config import Settings
import sys

settings = Settings()
services = settings.get_service()

def docopt_service(command, argv):
   argv.insert(0, command)
   valid_args = set(services)
   args_doc = '\n   '.join(valid_args)
   doc = """usage:
   ceetools-ctl [options] %s [<args>...]

options:
   -h --help     Print this help message

%s the following processies with the controller:
   %s
""" % (command, command, args_doc)

   args = docopt(doc, argv=argv)
   if valid_args.issuperset(args['<args>']):
      return args
   else:
      sys.stderr.write(doc)
      sys.exit(1)

def docopt_build(command, argv):
   argv.insert(0, command)
   valid_args = set(services)
   args_doc = '\n   '.join(valid_args)
   doc = """usage:
   ceetools-ctl [options] %s [<args>...]

options:
   -h --help     Print this help message

%s the following processies with the controller:
   %s
""" % (command, command, args_doc)

   args = docopt(doc, argv=argv)
   if valid_args.issuperset(args['<args>']):
      return args
   else:
      sys.stderr.write(doc)
      sys.exit(1)

def docopt_tail(command, argv):
   argv.insert(0, command)
   valid_args = set(services)
   args_doc = '\n   '.join(valid_args)
   doc = """usage:
   ceetools-ctl [options] %s [--follow] [<args>...]

options:
   -h --help     Print this help message
   -F --follow   Stream output from container

%s the following processies with the controller:
   %s
""" % (command, command, args_doc)

   args = docopt(doc, argv=argv)

   if args['--follow']:
      args['<args>'] = {'follow': True, 'service': args['<args>']}
      return args

   elif valid_args.issuperset(args['<args>']):
      args['<args>'] = {'follow': False, 'service': args['<args>']}
      return args

   else:
      sys.stderr.write(doc)
      sys.exit(1)

def docopt_noargs(command, argv):
   argv.insert(0,command)
   doc = """usage:
   ceetools-ctl [options] %s

options:
   -h --help     Print this help message
""" % (command,)
   return docopt(doc,argv=argv)

def docopt_run(command, argv):
   argv.insert(0,command)
   doc = """usage:
   ceetools-ctl [options] %s <script>...

options:
   -h --help     Print this help message
""" % (command,)

   return docopt(doc, argv=argv)
