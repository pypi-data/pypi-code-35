from setuptools import setup, find_packages

setup(
    name='ss-py',
    version='2019.3.19.0',
    license="MIT Licence",
    description="SS Tool",

    author='YaronH',
    author_email="yaronhuang@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["aigpy >= 1.0.40", "python-iptables"],

    entry_points={'console_scripts': [
        'ss-py = ss_py:main', ]}
)
