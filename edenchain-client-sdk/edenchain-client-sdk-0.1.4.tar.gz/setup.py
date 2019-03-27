from setuptools import setup, find_packages
import eden_client_api as api

setup(name='edenchain-client-sdk', version=api.__version__, description='edenchain client sdk',  author='Edenpartners', author_email='tech@edenchain.io', license='MIT', packages= find_packages() , 
        install_requires=[
            'requests',
            'base58',
            'cryptoconditions',
            'python-rapidjson',
            'pysha3',
            'eth_account'
        ],
        py_modules=['eden_client_api'],
        keyword=['edenchain','api','sdk'],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
        ],
        zip_safe=False)
