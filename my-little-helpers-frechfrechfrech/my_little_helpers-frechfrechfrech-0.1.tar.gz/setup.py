import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='my_little_helpers-frechfrechfrech',
      version='0.1',
      author='Alex Frech',
      author_email='frechfrechfrech@gmail.com',
      description='Functions that I use often',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/frechfrechfrech/helper_functions',
      license='MIT',
      packages=setuptools.find_packages(),
      install_requires = [
            'pandas==0.23.4',
            'numpy==1.14.3',
            'psycopg2==2.7.5',
            'mysqlclient==1.3.14',
            'matplotlib==2.2.2',
            'seaborn==0.9.0',
      ],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
