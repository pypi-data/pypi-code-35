from setuptools import setup, find_packages

setup( name='treep',
       version='1.2',
       description='managing git projects structured in tree in python',
       classifiers=[
           'License :: OSI Approved :: MIT License',
           'Programming Language :: Python :: 2.7',
           'Programming Language :: Python :: 3',
       ],
       data_files=["treep_documentation.txt"],
       keywords='project git tree',
       url='https://git-amd.tuebingen.mpg.de/amd-clmc/treep',
       author='Vincent Berenz',
       author_email='vberenz@tuebingen.mpg.de',
       license='GPL',
       packages=['treep'],
       install_requires=['lightargs','colorama','gitpython','argcomplete','pyyaml'],
       scripts=['bin/treep','bin/treep_to_yaml'],
       include_package_data=True,
       zip_safe=False
)



