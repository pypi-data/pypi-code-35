import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(name='pycountdict',
                 version='1.0.4',
                 author='bjtj',
                 author_email='bjtj10@gmail.com',
                 description='python counter dictionary',
                 long_description=long_description,
                 long_description_content_type='text/markdown',
                 url='https://github.com/bjtj/python-counter-dictionary',
                 packages=setuptools.find_packages(),
                 classifiers=[
                     'Programming Language :: Python :: 3',
                     'License :: OSI Approved :: MIT License',
                     'Operating System :: OS Independent',
                 ],
)
