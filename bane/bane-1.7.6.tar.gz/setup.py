import setuptools,os,platform,sys
with open("README.md", "r") as fh:
    long_description = fh.read()
'''
i made this so you can use it on termux :)
'''
req=["requests","lxml","PySocks","bs4","paramiko","pexpect","mysql-connector","scapy","stem"]

if (sys.platform == "win32") or( sys.platform == "win64"):
 req=["requests","lxml","PySocks","bs4","paramiko","mysql-connector","scapy","stem"]

if os.name=='posix':
 if platform.linux_distribution()==('','',''):
  req=["requests","lxml","PySocks","bs4","pexpect","mysql-connector","scapy","stem"]
    
setuptools.setup(
    name="bane",
    version="1.7.6",
    author="AlaBouali",
    author_email="trap.leader.123@gmail.com",
    description="cyber security library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlaBouali/bane",
    python_requires=">=2.7",
    install_requires=req,
    packages=["bane"],
    license="MIT License",
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License ",
        "Operating System :: Unix",
    ],
)
