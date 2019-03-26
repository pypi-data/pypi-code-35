from setuptools import setup

try:
    long_description = open('README.md', encoding='utf8').read()
except:
    long_description = 'python registry package',

setup(
    name='py_configs_registry',
    version='0.0.2',
    description='python registry package',
    long_description=long_description,
    long_description_content_type="text/markdown",

    py_modules=["registry"],

    url='http://github.com/ztj1993/py_configs_registry',
    author='ZhangTianJie',
    author_email='ztj1993@gmail.com',

    keywords='registry config json yaml',
    install_requires=['mergedict'],

    license='MIT',
)
