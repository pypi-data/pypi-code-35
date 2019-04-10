from distutils.core import setup
import wheel

setup(
    # Application name:
    name="libprime",

    description=' A library to manipulate prime numbers',
    #README='README.txt',
    #readme='README.txt',
    # Version number (initial):
    version="0.0.1b1",

    # Application author details:
    author="shankar",
    author_email='shankar162003@gmail.com',

    #license='LICENSE.txt',
    #LICENSE='LICENSE.txt',
    
    
    # Packages
    packages=["libprime"],

    # Include additional files into the package
    #include_package_data=True,

    # Details
    url="http://pypi.python.org/pypi/libprime",

    classifiers=['License :: OSI Approved :: BSD License',
                 'Framework :: IDLE',
                 'Development Status :: 2 - Pre-Alpha',
                 'Environment :: Console',
                 'Intended Audience :: Developers',
                 'Natural Language :: English',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 3.4',
                 'Topic :: Security :: Cryptography'
                 

                 
                 ],
 
    
    
    

    # Dependent packages (distributions)
   
)
