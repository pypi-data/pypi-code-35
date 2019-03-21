from setuptools import setup, find_packages


setup(name='x-mroy-0',
    version='0.0.1',
    description='a manager package',
    url='https://github.com/Qingluan/xproj.git',
    author='Qing luan',
    author_email='darkhackdevil@gmail.com',
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    packages=find_packages(),
    install_requires=['gitpython','termcolor','tqdm', 'mroylib-min'],
    entry_points={
        'console_scripts': ['x-proj=xproj_src.cmd:main']
    },

)
