from setuptools import find_packages, setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='mgl_efis_plotter',
      version='0.2.1',
      description='MGL EFIS data plotter',
      long_description=readme(),
      long_description_content_type="text/x-rst",
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      url='https://github.com/azemon/mgl_efis_plotter',
      author='Art Zemon',
      author_email='art@zemon.name',
      license='MIT',
      packages=find_packages(),
      install_requires=['matplotlib', 'pandas'],
      zip_safe=False
      )
