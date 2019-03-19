from setuptools import find_packages, setup
setup(
    name='HeadFirstPython',
    version='0.0.1',
    description='Python REST API client for Guacamole 0.9.13 version',
    author='right_now',#作者
    author_email='1051136665@qq.com',
    url='https://github.com/ChenBin113',
    # packages=find_packages(),
    packages=['HeadFirstPython'],  #这里是所有代码所在的文件夹名称
    install_requires=['requests'],
)