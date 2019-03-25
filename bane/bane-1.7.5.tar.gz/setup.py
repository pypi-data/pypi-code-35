import setuptools,sys
with open("README.md", "r") as fh:
    long_description = fh.read()
'''
i made this so you can use it on termux, if you are not a termux user you can install: "paramiko" and enjoy all the features :)
'''
if (sys.platform != "win32") and( sys.platform != "win64"):
    req=["requests","lxml","PySocks","bs4","pexpect","mysql-connector","scapy","stem"]
else:
    req=["requests","lxml","PySocks","bs4","paramiko","pexpect","mysql-connector","scapy","stem"]
setuptools.setup(
    name="bane",
    version="1.7.5",
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
