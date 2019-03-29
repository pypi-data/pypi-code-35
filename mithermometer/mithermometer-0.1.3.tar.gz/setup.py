"""Python package description."""
from setuptools import setup, find_packages


def readme():
    """Load the readme file."""
    with open('README.md', 'r') as readme_file:
        return readme_file.read()


setup(
    name='mithermometer',
    version='0.1.3',
    description='Library to read data from Xiaomi Aqara thermometer',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/hobbypunk90/mithermometer',
    author='Marcel Hoppe',
    author_email='hoppe.marcel@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: System :: Hardware :: Hardware Drivers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    packages=find_packages(),
    keywords='thermometer temperature humidity sensor bluetooth low-energy ble',
    zip_safe=False,
    install_requires=['btlewrap==0.0.4'],
    extras_require={'testing': ['pytest']},
    include_package_data=True,
)
