import setuptools

with open('README.md', 'r') as f:
    description = f.read()

setuptools.setup(
    name='anna_node',
    version='1.1.7',
    author='Patrik Pihlstrom',
    author_email='patrik.pihlstrom@gmail.com',
    url='https://github.com/patrikpihlstrom/anna',
    description='simulated & automated end-to-end website testing software',
    long_description=description,
    long_description_content_type='text/markdown',
    packages=['anna', 'anna.driver'],
    install_requires=[
        'selenium',
        'anna_common',
        'anna_client',
        'anna_unittasks'
    ]
)
