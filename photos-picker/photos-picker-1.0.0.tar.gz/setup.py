import os
from setuptools import setup, find_packages

github_url = 'https://github.com/l-vo/photos-picker'
version = '1.0.0'


def read(fname):
    content = open(os.path.join(os.path.dirname(__file__), fname)).read()
    return content.replace('doc/', github_url + '/blob/' + version + '/doc/')


setup(
    name='photos-picker',
    version=version,
    description='Pick photos following a given strategy '
                'and upload them to various destinations',
    author='Laurent VOULLEMIER',
    author_email='laurent.voullemier@gmail.com',
    url=github_url,
    packages=find_packages(),
    install_requires=['Pillow', 'zope.event', 'dropbox', 'pydrive'],
    include_package_data=True,
    zip_safe=False,
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    license='MIT',
    keywords='photos upload photoframe',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2'
    ]
)
