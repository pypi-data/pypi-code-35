from setuptools import setup

setup(
    name='0x01-autocert-dns-aliyun',
    version='0.1',
    description='Aliyun DNS plugin for autocert project',
    url='https://github.com/Smart-Hypercube/autocert',
    author='Hypercube',
    author_email='hypercube@0x01.me',
    license='MIT',
    py_modules=['autocert_dns_aliyun'],
    python_requires='>=3.6',
    install_requires=['aliyun-python-sdk-alidns>=2.0.7'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
