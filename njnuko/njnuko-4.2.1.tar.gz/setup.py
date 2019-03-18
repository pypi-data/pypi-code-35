import setuptools
with open("README.md","r") as fh:
      long_description=fh.read()



setuptools.setup(
      name="njnuko",
      version="4.2.1",
      description="file sorting",
      author='njnuko',
      author_email='njnuko@163.com',
      url='https://github.com/njnuko/njnuko',
      license='MIT',
      packages=setuptools.find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=['psycopg2','pymysql','filetype'],
      entry_points="",
      )
