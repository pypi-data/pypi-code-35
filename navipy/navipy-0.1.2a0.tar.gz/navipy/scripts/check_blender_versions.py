from platform import python_version
import os


packages = ['numpy',
            'pandas',
            'matplotlib',
            'scipy',
            'networkx',
            'ipython',
            'yaml',
            'PIL',
            'cv2',
            'fastdtw']
filereq = 'requirement.txt'
# Look for packages require by blender and navipy
# there versions should match
requirements = []
print('Look for packages')
for pkg in packages:
    try:
        cmod = __import__(pkg)
    except ImportError as e:
        # Not use by blender so no incompatibilty issues
        continue
    try:
    	line = pkg + '==' + cmod.__version__
    except AttributeError as e:
        #Package as no __version__
        continue
    print('\t', line)
    requirements.append(line)
# Write a requirement file to auto install the packages
# prior to navipy with the correct versions
with open(filereq, 'w') as cfile:
    for line in requirements:
        cfile.write(line + '\n')
print('Requirement file written... Ok')

# Display user informations
pythonvec = python_version()
pathreq = os.path.abspath(filereq)
print('You can create an anaconda virtual environment as follow')
print('\t conda update conda')
print('\t conda create -n myblendnavipy python={} anaconda'.format(
    pythonvec))
print('\t activate myblendnavipy')
print('\t conda install --yes --file {}'.format(pathreq))
print('\t conda install navipy')
