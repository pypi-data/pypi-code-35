from setuptools import setup

with open('README.md', 'r') as in_file:
    readme = in_file.read()

setup(
    name='occamtools',
    packages=['occamtools'],
    url='https://github.com/mortele/OccamTools',
    license='GPL-3',
    description='Analysis and synthesis tools for OCCAM hPF simulations',
    long_description=readme,
    long_description_content_type='text/markdown',
    tags=['occammd', 'hpf', 'md'],
    author='Morten Ledum',
    author_email='morten.ledum@gmail.com',
    install_requires=[
        'pytest>=4.3.0',
        'pytest-cov>=2.6.1',
        'scikit-learn>=0.20.2',
        'scipy>=1.2.1',
        'numpy>=1.16.1',
        'numba>=0.42.1',
        'matplotlib>=3.0.2',
        'flake8>=3.7.7',
        'coverage>=4.5.2',
        'tqdm>=4.31.1'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    python_requires='>=3.6',
    use_scm_version=True,
    setup_requires=['setuptools_scm']
)
