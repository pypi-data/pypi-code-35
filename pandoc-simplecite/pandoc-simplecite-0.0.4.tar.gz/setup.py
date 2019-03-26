import setuptools

LONG_DESCRIPTION = """\
A pandoc filter providing simple citation of documents for markdown files.
"""

VERSION = '0.0.4'

setuptools.setup(
    name='pandoc-simplecite',
    version = VERSION,

    author = 'Walter Stocker',
    author_email='wrstocke@googlemail.com',
    description = 'Simple citation filter for pandoc',
    long_description = LONG_DESCRIPTION,
    license='MIT',
    keywords='pandoc cite simple filter',
    url='https://gitlab.com/walter76/pandoc-simplecite',

    py_modules=['pandoc_simplecite'],
    entry_points={'console_scripts':['pandoc-simplecite = pandoc_simplecite:main']},

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Documentation',
        'Topic :: Text Processing :: Filters'
    ]
)