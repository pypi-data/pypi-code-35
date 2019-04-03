from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()
 
setup(name='lrucachenivkum',
      version='0.1',
      url='https://github.com/Niveditha-kumaran/lrucachenivkum',
      license='MIT',
      author='Niveditha Kumaran',
      author_email='nov28niv@gmail.com',
      packages=['lrucachenivkum'], 
      description='LRU cache implementation',
      zip_safe=False)