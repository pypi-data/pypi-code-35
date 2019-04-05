from setuptools import setup


classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Topic :: Software Development :: Libraries',
]

setup(
    name='corva-worker-python',
    author='Jordan Ambra',
    author_email='jordan.ambra@corva.ai',
    url='https://bitbucket.com/corva/corva-worker-python',
    version='0.1.1',
    classifiers=classifiers,
    description='SDK for interacting with Corva',
    keywords='corva',
    packages=["worker"],
    install_requires=[],
    include_package_data=True,
    license='The Unlicense',
)
