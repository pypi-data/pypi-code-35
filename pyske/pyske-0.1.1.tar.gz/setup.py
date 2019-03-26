import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='pyske',  
     version='0.1.1',
     scripts=['psk'] ,
     license='MIT',
     author="Jolan Philippe and Frederic Loulergue",
     author_email="jp2589@nau.edu, frederic.loulergue@nau.edu",
     description="A package for Python Skeletons using mpi4py",
     long_description=long_description,
   long_description_content_type="text/markdown",
     packages=  setuptools.find_packages(),
     install_requires=['mpi4py'],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
