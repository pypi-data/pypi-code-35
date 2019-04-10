import re
from subprocess import check_call, PIPE
from setuptools import setup, find_packages


try:
    check_call(["surfraw", "-h"], stdout=PIPE)
except:
    print("Please install surfraw to use this.")



def get_version(project_name):
    regex = re.compile(r"""^__version__ = ["'](\d+\.\d+\.\d+(?:a|b|rc)?(?:\d)*?)["']$""")
    with open("{}/__init__.py".format(project_name)) as f:
        for line in f:
            m = regex.match(line.rstrip("\n"))
            if m is not None:
                return m.groups(1)[0]


def convert_images(text):
    image_regex = re.compile(r"!\[(.*?)\]\((.*?)\)")
    return image_regex.sub(r'<img src="\2" alt="\1">', text)


class About(object):
    NAME='search-cli'
    VERSION=get_version('search')
    AUTHOR='blester125'
    EMAIL='{}@gmail.com'.format(AUTHOR)
    URL='https://github.com/{}/{}'.format(AUTHOR, NAME)
    DL_URL='{}/archive/{}.tar.gz'.format(URL, VERSION)
    LICENSE='MIT'
    DESCRIPTION='Search'


ext_modules = [
]

setup(
    name=About.NAME,
    version=About.VERSION,
    description=About.DESCRIPTION,
    long_description=convert_images(open('README.md').read()),
    long_description_content_type="text/markdown",
    author=About.AUTHOR,
    author_email=About.EMAIL,
    url=About.URL,
    download_url=About.DL_URL,
    license=About.LICENSE,
    packages=find_packages(),
    package_data={
        'search_cli': [
        ],
    },
    include_package_data=True,
    install_requires=[
    ],
    setup_requires=[
    ],
    extras_require={
        'test': ['pytest'],
    },
    keywords=[],
    ext_modules=ext_modules,
    entry_points={
        'console_scripts': [
            'search=search.search:main',
            'sr=search.search:main',
            'search_highlighted=search.search:search_highlighted',
            'search_gui=search.search_gui:search_gui',
            'search_gui_highlighted=search.search_gui:search_gui_highlighted',
        ],
    },
    classifiers={
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering',
    },
)
