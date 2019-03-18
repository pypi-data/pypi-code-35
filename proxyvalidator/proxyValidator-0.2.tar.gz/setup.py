import setuptools
setuptools.setup(
     name='proxyValidator',  
     version='0.2',
     author="Zygimantas Bagdzevicius",
     author_email="zbagdzevicius@gmail.com",
     description="Returns validated proxies",
     url="https://github.com/zbagdzevicius/proxyValidator",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     install_requires=[
         'requests',
     ],
 )