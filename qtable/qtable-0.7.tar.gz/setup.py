from setuptools import setup, find_packages
setup(
      name="qtable",
      version = "0.7",
      description="handle,.in progressing..,APIs",
      author="dapeli",
      url="https://github.com/ihgazni2/qtable",
      author_email='terryinzaghi@163.com', 
      license="MIT",
      long_description = "refer to .md files in https://github.com/ihgazni2/qtable",
      classifiers=[
          'Environment :: Console',
          'Environment :: Web Environment',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'Programming Language :: Python',
          ],
      packages= find_packages(),
      py_modules=['qtable'], 
      )


# python3 setup.py bdist --formats=tar
# python3 setup.py sdist

