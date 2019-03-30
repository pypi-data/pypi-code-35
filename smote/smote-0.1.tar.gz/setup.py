from setuptools import setup
setup(name='smote',
      version='0.1',
      description='',
      url='https://github.com/chupati/smote',
      author='David N. Sanchez',
      author_email='dsanchez@dnsai.io',
      license='MIT',
      packages=['smote'],
      install_requires=['numpy>=1.14.3',
                        'scikit-learn>=0.19.1'])