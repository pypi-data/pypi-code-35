import setuptools

with open('readme.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'mezzanine_cartridge_api',
    version = '1.0.0',
    author = 'Jack van Zyl',
    author_email = 'jackvanzyl@icloud.com',
    description = 'A REST Web API for Mezzanine CMS with the Cartridge e-commerce extension',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/jackvz/mezzanine-cartridge-api',
    packages = setuptools.find_packages(),
    install_requires=[
        'django-oauth-toolkit==1.1.1',
        'django-cors-middleware==1.3.1',
        'djangorestframework==3.9.2',
        'djangorestframework-api-key==0.3.1',
        'django-rest-swagger==2.2.0',
    ],
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)