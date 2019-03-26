
SETUP_INFO = dict(
    name = 'infi.recipe.js_requirements',
    version = '0.2.2',
    author = 'fanchi',
    author_email = 'rbelio@infinidat.com',

    url = 'https://github.com/Infinidat/infi.recipe.js_requirements',
    license = 'BSD',
    description = """buildout recipe for downloading, extracting and dependency parsing for JavaScript""",
    long_description = """buildout recipe for downloading, extracting and dependency parsing for JavaScript""",

    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    install_requires = [
'setuptools>=32.0',
'zc.buildout',
'semantic_version',
'six',
'requests'
],
    namespace_packages = ['infi', 'infi.recipe'],

    package_dir = {'': 'src'},
    package_data = {'': []},
    include_package_data = True,
    zip_safe = False,

    entry_points = {
        'console_scripts': [],
        'gui_scripts': [],
        'zc.buildout': ['default = infi.recipe.js_requirements:JSDep']
        }
)

if SETUP_INFO['url'] is None:
    _ = SETUP_INFO.pop('url')

def setup():
    from setuptools import setup as _setup
    from setuptools import find_packages
    SETUP_INFO['packages'] = find_packages('src')
    _setup(**SETUP_INFO)

if __name__ == '__main__':
    setup()

