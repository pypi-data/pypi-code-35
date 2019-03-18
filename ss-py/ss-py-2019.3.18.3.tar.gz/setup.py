from setuptools import setup, find_packages

setup(
    name='ss-py',
    version='2019.3.18.3',
    license="MIT Licence",
    description="SS Tool",

    author='YaronH',
    author_email="yaronhuang@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["aigpy >= 1.0.39"],

    entry_points={'console_scripts': [
        'ss-py = ss_py:main', ]}
)
