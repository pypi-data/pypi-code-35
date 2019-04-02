from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='simple_helpers',
      version='0.1.1',
      description='A collection of helper functions',
      long_description=readme(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python :: 3.7',
          'Topic :: Utilities'
      ],
      keywords='parallel-progress-bar parallel-computing progress-bar parallel',
      url='http://github.com/RHammond2/simple_helpers',
      author='Rob Hammond',
      author_email='reh388@nyu.edu',
      license='MIT',
      packages=['simple_helpers'],
      install_requires=[
          'tqdm'
      ],
      include_package_data=True,
      zip_safe=False)
