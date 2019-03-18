from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='tnprofanity',
    version='0.3.2',
    description='thai-text profanity library',
    long_description=readme(),
    url='',
    author='GarKoZ',
    author_email='gark36@gmail.com',
    license='MIT',
    install_requires=[

    ],
    scripts=[],
    keywords='thai english profanity censor',
    packages=['tnprofanity'],
    package_dir={'tnprofanity': 'src/tnprofanity'},
    package_data={'tnprofanity': ['*']}
)