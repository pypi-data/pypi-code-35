from setuptools import setup

setup(
    name='TRecord',
    version='1.0.0',
    packages=['trecord'],
    url='https://github.com/lusaisai/TRecord',
    license='MIT',
    author='lusaisai',
    author_email='lusaisai@163.com',
    description='An Interactive SQL Client',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pygments',
        'PyMySQL',
        'pyodbc',
        'cx_Oracle',
        'prompt_toolkit',
        'tabulate[widechars]',
        'tablib',
        'click'
    ],
    scripts=[
        'scripts/trecord'
    ]
)
