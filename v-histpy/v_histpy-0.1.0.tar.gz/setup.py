
import pathlib
from distutils.core import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
  name = 'v_histpy',        
  packages = ['v_histpy'],
  version = '0.1.0',
  license='MIT',    
  description = 'Create quick histograms that fit the terinal', 
  long_description = README, 
  long_description_content_type = 'text/markdown',
  author = 'John Naylor',               
  author_email = 'jonaylor89@gmail.com',      
  url = 'https://github.com/jonaylor89/v_histpy',
  download_url = 'https://github.com/jonaylor89/v_histpy/archive/v_1.0.tar.gz',
  keywords = ['hist', 'v_hist','terminal', 'formatting'],   
  entry_points={"console_scripts": ["hist=v_histpy.hist:main"]},
  classifiers=[
    'Development Status :: 3 - Alpha',  

    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',

    'License :: OSI Approved :: MIT License',

    'Programming Language :: Python :: 3',  
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
