from distutils.core import setup
setup(
  name = 'Praat_feature',         # How you named your package folder (MyLib)
  packages = ['Praat_feature'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Extraction of Prosodic features with PRAAT',   # Give a short description about your library
  author = 'Rajesh Marandi',                   # Type in your name
  author_email = 'rajesh.marandi@quantiphi.com',      # Type in your E-Mail
  url = 'https://gitlab.com/rajesh.marandi/praat_features/tree/for_pip',   # Provide either the link to your github or to your website
  keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'praat-parselmouth',
          'scipy==1.1.0',
          'numpy==1.15.2',
          'flask==1.0.2',
          'pandas==0.23.0'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)

