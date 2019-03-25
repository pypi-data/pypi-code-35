try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
setup(
    name='runner-easyuiautomator',
    version='1.3',
    url='',
    license='',
    author='thomas.ning',
    author_email='',
    description='',
    packages=['runner', 'runner.common','runner.application'],
    package_data={
        'runner': [
            'application/resources/*.html'
        ]
    },
    include_package_data=True,
    zip_safe=False
)