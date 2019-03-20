from setuptools import setup
def readme():
    with open('README.rst') as f:
        return f.read()
setup(name='moniotclient',
      version='1',
      description='IOT client',
      url='http://github.com/ayhant',
      long_description="MIT Lıcense",
      long_description_content_type="text/x-rst",
      author='Ayhan Taşyurt',
      author_email='ayhantsyurt@gmail.com',
      license='MIT',
      packages=['moniotclient'],
      install_requires=["paho-mqtt"],
      zip_safe=False)