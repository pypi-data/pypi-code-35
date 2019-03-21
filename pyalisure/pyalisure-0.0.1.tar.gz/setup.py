from setuptools import setup, find_packages

setup(name='pyalisure', version="0.0.1",
      description='写程序的时候发现有很多常用的方法，每次都需要实现，因此我把这些功能抽取出来，写成一个pyhton包并发布出来。',
      long_description=open('README.rst').read(),
      author='ALISURE',
      author_email='562282219@qq.com',
      maintainer='ALISURE',
      maintainer_email='562282219@qq.com',
      license='BSD License',
      packages=find_packages(),
      platforms=["all"],
      url='https://github.com/alisure-ml/pyalisure',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Operating System :: OS Independent',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python',
          'Programming Language :: Python :: Implementation',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries'],
      install_requires=[

      ])
