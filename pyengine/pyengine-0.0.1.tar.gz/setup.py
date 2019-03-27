#encoding=utf-8
from setuptools import setup, find_packages

setup(
    name = "pyengine",
    version = "0.0.1",
    keywords = ["py", "engine","run"],
    description = '''
    继承这个包中的FuncClass写一个它的子类,重写它的predict方法可以从/register/接口来动态运行这个predict方法,
    然后通过post方式将代码放入请求的body体中，就可以动态运行这个方法。可以通过/add/和/reduce/减少可以可以同时存在的子类数量。
    启动工程方法 实例 pyengine run -p 5000 -n 50
    ''',
    long_description = "eds sdk for python",
    license = "Apache License V2.0",

    url = "http://www.gitee.com",
    author = "liuyancong",
    author_email = "1437255447@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['Flask==1.0.2','Flask-Script==2.0.6'],

    scripts = [],
    entry_points = {
        'console_scripts': [
            'pyengine = pyengine.app:main'
        ]
    }
)
