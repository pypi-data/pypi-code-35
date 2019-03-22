from setuptools import setup
setup(
        name='NNGA', 
        version='0.0.4', 
        description='A neural networks combine genetic algorithm module.',
        long_description=open('README.rst').read(),
        author='maigua', 
        author_email='3075489925@qq.com',
        py_modules=['neuralNetworkGA'],
        install_requires=[
        'random',
        'numpy',
        'shelve'
        ]
)