import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='crawlerUtils',
    version='1.8.1.post2',
    description='Crawler Utils examples',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='crawler html selenium-python python3 requests beautifulsoup4 urllib mail schedule captcha excel scraping log requests-html csv gevent spiders geohash base64',
    install_requires=[
        "bs4>=0.0.1",
        "selenium>=3.141.0",
        "schedule>=0.6.0",
        "xlrd>=1.2.0",
        "xlwt>=1.3.0",
        "gevent>=1.4.0",
        "requests-html>=0.10.0",
        "Pillow>=5.3.0",
    ],
    packages=setuptools.find_packages(),
    author='Tyrone Zhao',
    author_email='tyrone-zhao@qq.com',
    url='https://github.com/Tyrone-Zhao/crawlerUtils',
    python_requires='>=3.6.0',
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable'
        'Development Status :: 3 - Alpha',  # 当前开发进度等级（测试版，正式版等）
        'Intended Audience :: Developers',  # 模块适用人群
        'Topic :: Software Development :: Code Generators',  # 给模块加话题标签
        'License :: OSI Approved :: MIT License',  # 模块的license

        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python',
        # 'Programming Language :: Python :: Implementation :: CPython',
        # 'Programming Language :: Python :: Implementation :: PyPy',
    ],
    project_urls={  # 项目相关的额外链接
        'Blog': 'https://blog.csdn.net/weixin_41845533',
    },
)


# cd GitHub/crawlerUtils && rm -rf dist/* && python setup.py sdist bdist_wheel
# twine upload dist/* --skip-existing
# pip install --user --upgrade crawlerUtils

# include pat1 pat2 ...   #include all files matching any of the listed patterns
# exclude pat1 pat2 ...   #exclude all files matching any of the listed patterns
# recursive-include dir pat1 pat2 ...  #include all files under dir matching any of the listed patterns
# recursive-exclude dir pat1 pat2 ... #exclude all files under dir matching any of the listed patterns
# global-include pat1 pat2 ...    #include all files anywhere in the source tree matching — & any of the listed patterns
# global-exclude pat1 pat2 ...    #exclude all files anywhere in the source tree matching — & any of the listed patterns
# prune dir   #exclude all files under dir
# graft dir   #include all files under dir

# 删除敏感信息
# git filter-branch --index-filter 'git rm -r --cached --ignore-unmatch src/main/resources/passowrd.txtx' HEAD
# git reflog expire --expire=now --all
# git gc --prune=now
# git gc --aggressive --prune=now
# git push --all --force