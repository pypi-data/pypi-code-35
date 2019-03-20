from distutils.core import setup

setup(
    name = 'CNExpir',      
    version = '0.0.2',
    author = 'vlsee',        
    author_email = '1223589209@qq.com',
    url = 'https://github.com/mizao/CNExpir',
    description=(
        '实现离散SI,SIR扩散过程,Price网络生成'
    ),
    long_description=open('README').read(),
    packages=['CNExpir']
)