from setuptools import find_packages, setup

with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name='apiage',
    version='0.1.4',
    description='Gets pages from API.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/mindey/apiage',
    author='Mindey',
    author_email='mindey@qq.com',
    license='UNDEFINED',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires=["requests", "progress", "furl", "goto-statement"],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    zip_safe=False
)

