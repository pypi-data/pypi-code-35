
from setuptools import setup, find_packages


setup(name='x_xmlparse',
    version='0.0.5',
    description='None',
    url='https://github.com/xxx',
    author='auth',
    author_email='xxx@gmail.com',
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    packages=find_packages(),
    install_requires=['lxml','termcolor', 'cssselect', 'requests', 'requests[socks]'],
    entry_points={
        'console_scripts': ['xq=x_xmlparse_src.cmd:main', 'eq=x_xmlparse_src.cmd_xlsx:main',]
    },

)
