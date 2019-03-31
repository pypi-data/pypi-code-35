import setuptools

import timer


def _read(filename):
    with open(filename, encoding='UTF-8') as ifs:
        return ifs.read()


setuptools.setup(
    name=timer.APP,
    version=timer.VERSION,
    author='Fenglei Zhang',
    author_email='fenglei4518@hotmail.com',
    description='A better count-down timer in tkinter',
    long_description=_read('README.md'),
    long_description_content_type='text/markdown',
    url=timer.SITE,
    keywords=['countdown', 'timer', 'tkinter'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
        'Topic :: Office/Business'
    ],
    python_requires='>=3.6',
    packages=setuptools.find_packages(),
    entry_points={
        'gui_scripts': [
            '%s=timer.App:main' % timer.APP
        ]
    },
    include_package_data=True,
    package_data={
        'timer.resource': ['image/*']
    },
    platforms=['any']
)
