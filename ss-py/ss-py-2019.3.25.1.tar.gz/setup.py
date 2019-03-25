from setuptools import setup, find_packages

setup(
    name='ss-py',
    version='2019.3.25.1',
    license="MIT Licence",
    description="SS Tool",

    author='YaronH',
    author_email="yaronhuang@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["aigpy >= 2019.3.21.0", "netfilter"],

    entry_points={'console_scripts': [
        'ss-py = ss_py:main', ]}
)
