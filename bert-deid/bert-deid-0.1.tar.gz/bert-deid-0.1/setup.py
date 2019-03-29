import setuptools

def readme():
    with open('README.md') as f:
        return f.read()

setuptools.setup(name='bert-deid',
      version='0.1',
      description='Remove identifiers from data with BERT',
      url='https://github.com/MIT-LCP/pydeid',
      license='MIT',
      packages=setuptools.find_packages(),
      install_requires=[]
          )
