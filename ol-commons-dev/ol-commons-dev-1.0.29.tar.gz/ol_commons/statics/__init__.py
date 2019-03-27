import os.path
prog = __file__
directory = os.path.dirname(os.path.abspath(prog))
print(os.path.join(directory, 'logging.yaml'))
