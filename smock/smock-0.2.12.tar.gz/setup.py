from distutils.core import setup
import pathlib

HERE = pathlib.Path(__file__).parent

try:
    README = (HERE / "README.md").read_text()
except:
    README = ""

setup(
  name='smock',
  packages=['smock'],  # this must be the same as the name above
  version='0.2.12',
  description='Serverboards Mock library',
  author='David Moreno',
  author_email='dmoreno@serverboards.io',
  url='https://github.com/serverboards/smock',
  keywords=['testing', 'mock', 'mocking'],
  install_requires=["PyYAML"],
  classifiers=[],
  license="Apache2",
  long_description=README,
  long_description_content_type="text/markdown",
)

# to upload to pypi:
# python3 setup.py sdist
# twine upload dist/LATEST.tgz
