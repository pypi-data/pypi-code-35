from distutils.core import setup

setup(
    name='ybc_funny',
    version='1.1.0',
    description='Get The Funny Text',
    long_description='Get The Funny Text',
    author='zhangyun',
    author_email='zhangyun@fenbi.com',
    keywords=['pip3', 'python3', 'python', 'brain', 'funny', 'joke'],
    url='http://pip.zhenguanyu.com/',
    packages=['ybc_funny'],
    package_data={'ybc_funny': ['*.py']},
    license='MIT',
    install_requires=[
        'ybc_exception'
    ]
)
