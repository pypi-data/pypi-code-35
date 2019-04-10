from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "qvstbus",      #这里是pip项目发布的名称
    version = "0.0.6",  #版本号，数值大的会优先被pip
    
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["websocket-client"]          #这个项目需要的第三方库
)
