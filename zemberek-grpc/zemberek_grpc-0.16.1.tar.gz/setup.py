from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='zemberek_grpc',
      version='0.16.1',
      description='Requests to Zemberek gRPC server',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/ahmetaa/zemberek-nlp',
      author='Ahmet A. Akın, Mehmet D. Akın',
      author_email='ahmetaa@gmail.com',
      license="Apache License 2.0",
      packages=find_packages(),
      install_requires=[
          'grpcio-tools', 'grpcio', 'googleapis-common-protos'
      ],
      zip_safe=True,
      classifiers=(
        "Programming Language :: Python",
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Natural Language :: Turkish",
        "Programming Language :: Java",
        "Topic :: Text Processing",
      ),
      keywords='türkçe turkish language zemberek text',
)