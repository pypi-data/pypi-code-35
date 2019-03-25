from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='gitlab-webhook-telegram',
      version='1.0.1',
      description='A simple bot reacting to gitlab webhook',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='http://github.com/nanoy42/gitlab-webhook-telegram',
      author='Yoann `Nanoy` Pietri',
      author_email='me@nanoy.fr',
      license='GNU General Public License v3.0',
      packages=['gwt'],
      zip_safe=False,
      install_requires=['docopt', 'python-telegram-bot'],
      scripts=['bin/gwt'],
      include_package_data=True,
)
