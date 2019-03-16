# With inspiration from answers to code from StackOverflow
# https://stackoverflow.com/questions/1057431/how-to-load-all-modules-in-a-folder

__all__ = []

import os
for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    __all__.append(module[:-3])
del module
del os
