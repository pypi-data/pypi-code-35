from distutils.core import setup

setup(
    name='uk_postcodes',  # How you named your package folder (MyLib)
    packages=['uk_postcodes'],  # Chose the same as "name"
    version='0.1.1',  # Start with a small number and increase it with every change you make
    license='mit  ',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='The following library contains a simple library for validating and formatting the UK-postcodes.',
    # Give a short description about your library
    author='Pankaj Sonar',  # Type in your name
    author_email='pankaj.sonar@ucdconnect.ie',  # Type in your E-Mail
    url='https://github.com/pankajsonar19/uk-postcodes-library',
    # Provide either the link to your github or to your website
    download_url='https://github.com/pankajsonar19/uk-postcodes-library/archive/0.1.1.tar.gz',  # I explain this later on
    keywords=['ukpostcodes', 'uk', 'postcodes', 'europe','european union','postcode','formatting','validation','validating'],  # Keywords that define your package best
    install_requires=[  # I get to this in a second
        'pickle',
        'pandas',
        'glob'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
