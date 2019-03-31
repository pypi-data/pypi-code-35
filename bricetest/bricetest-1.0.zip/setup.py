from distutils.core import setup

setup(
    name= 'bricetest',
    version='1.0',
    author_email='xiaoxiaofeng1119@163.com',
    url='https://github.com/xiaoxiaofeng999/dabao_test2.git/',
    description= 'this is a test lib',
    license='MIT', 
    packages = ['test_package','test_package.test_package2']
)
