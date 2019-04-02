"""setup.py"""
import setuptools

setuptools.setup(
    name='apt-yikes',
    version='0.0.1',
    license='MIT',
    author='yiwen song',
    author_email='songzgy@gmail.com',
    url='https://github.com/yiwensong/ubuntu-setup',
    description=(
        'Makes a script to set up ubuntu boxes.'
    ),
    packages=['script_gen'],
    install_requires=[
        'pyyaml',
    ],
    classifiers=[
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'console_scripts': [
            'generate-script=script_gen:main',
        ]
    },
)
