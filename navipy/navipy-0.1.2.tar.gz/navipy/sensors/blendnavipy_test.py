""" A small script to test if navipy can run under blender"""
try:
    import navipy  # noqa F401
except ModuleNotFoundError:  # noqa F821
    raise NameError(
        'navipy could not be imported within blender scripting tool. ' +
        'This script should be run with the command blendnavipy.' +
        'If you did, you need to check that either the virtual' +
        ' environment can be activated under blender, or that' +
        ' the path can be reached by blender')

print('Blender has been successfully imported')
