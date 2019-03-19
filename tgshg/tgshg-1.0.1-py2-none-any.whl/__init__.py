# name = "tgshg"
# from os.path import dirname, basename, isfile
# import glob
# modules = glob.glob(dirname(__file__)+"/*.py")
# __all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

# import os
# for module in os.listdir(os.path.dirname(r"C:\Maya 2018\Maya2018\Python\Lib\site-packages\tgshg\__init__.py")):
#     if module == '__init__.py' or module[-3:] != '.py':
#         continue
#     __import__(module[:-3], locals(), globals())
# del module

# for i in os.listdir(os.path.dirname(r"C:\Maya 2018\Maya2018\Python\Lib\site-packages\tgshg\__init__.py")):
#     print i