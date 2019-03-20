from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(name='chess-cli-bshio',
      version='0.0.1',
      author='Brandon Shimanek',
      author_email='brandon.j.shimanek@gmail.com',
      description='Cli game of chess',
      long_description=long_description,
      url='https://github.com/shimanekb/chess',
      packages=['chess', 'chess.app', 'chess.app.controller',
                'chess.app.view'],
      entry_points={
            'console_scripts': ['chess = chess.app.__main__:main']
          },
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: Apache Software License",
          "Operating System :: OS Independent",
          ],
      )
