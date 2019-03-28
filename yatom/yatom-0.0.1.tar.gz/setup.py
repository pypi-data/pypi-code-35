from setuptools import setup, find_packages

setup(
    name='yatom',
    version='0.0.1',
    url='https://gitlab.com/ergoithz/yatom',
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
