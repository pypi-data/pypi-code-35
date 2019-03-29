from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='yatom',
    version='0.0.2',
    url='https://gitlab.com/ergoithz/yatom',
    author='Felipe A. Hernandez',
    author_email='ergoithz@gmail.com',
    description='Beautiful HTML/XHTML/XML using YAML',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing :: Markup',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Text Processing :: Markup :: XML',
        ],
    packages=find_packages(),
    package_data={'yatom.tests.resources': ['*']},
    install_requires=['pyyaml', 'six'],
    test_suite='yatom.tests',
    tests_require=['pycodestyle', 'importlib_resources'],
    zip_safe=True,
    platforms='any',
    )
