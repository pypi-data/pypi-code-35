import setuptools

with open('README.md') as f:
    long_description = f.read()

setuptools.setup(name='es-template-manager',
                 version='1.0',
                 author='Alex Corvin',
                 author_email='accorvin@live.com',
                 description=('A utility for managing Elasticsearch index'
                              ' templates in source control'),
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url='https://github.com/accorvin/es-template-manager',
                 packages=setuptools.find_packages(),
                 install_requires=['requests'],
                 entry_points={
                     'console_scripts': [
                         ('es-template-manager = '
                          'es_template_manager.es_template_manager:main')
                     ]
                 })
