from setuptools import setup,find_packages

exec(open('modelchimp/version.py').read())

setup(
  name = 'modelchimp',
  packages = find_packages(),
  version = '0.5.2',
  description = 'Python client to upload the machine learning models data to the model chimp cloud',
  entry_points='''
        [console_scripts]
        datachimp=modelchimp.cli:cli
    ''',
  author = 'Samir Madhavan',
  author_email = 'samir.madhavan@gmail.com',
  url = 'https://www.modelchimp.com',
  keywords = ['modelchimp', 'ai', 'datascience'],
  install_requires=[
          'requests',
          'future',
          'six',
          'websocket-client==0.47.0',
          'pytz',
          'cloudpickle',
          'click',
      ],
  classifiers = [],
)
