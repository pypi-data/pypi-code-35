from setuptools import setup

setup(name='fastpandavro',
      version='1.1',
      description='Parallel conversion of Avro file to Pandas dataframe and conversion of pandas dataframe to avro file',
      url='https://github.com/deepakagrawal/fastpandavro',
      author='Deepak Agrawal',
      author_email='agrawal.deepankur@gmail.com',
      license='MIT',
      packages=['fastpandavro'],
      zip_safe=False,
      download_url='https://github.com/deepakagrawal/fastpandavro/archive/v1.1.tar.gz',
      install_requires=['fastavro', 'pandas', 'multiprocessing', 'joblib'])
