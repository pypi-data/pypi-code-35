from setuptools import find_packages, setup

setup(
    name='verslilietuva_driver',
    version='0.0.1',
    description='Versli Lietuva EDB controller.',
    url='https://github.com/drivernet/verslilietuva_driver',
    author='Mindey',
    author_email='mindey@qq.com',
    license='ASK FOR PERMISSIONS',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires=['metadrive'],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    zip_safe=False
)
