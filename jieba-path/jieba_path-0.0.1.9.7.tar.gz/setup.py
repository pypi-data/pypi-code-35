from setuptools import find_packages, setup
setup(
    name='jieba_path',
    version='0.0.1.9.7',
    description='结巴分词预处理目录下的文档',
    author='author',  # 作者
    author_email='napoler2008@gmail.com',
    url='https://www.terrychan.org/p/977',
    # packages=find_packages(),
    packages=['jieba_path'],  # 这里是所有代码所在的文件夹名称
    install_requires=['jieba'])

# python setup.py sdist
# #python setup.py install
# python setup.py sdist upload
