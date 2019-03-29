import setuptools

setuptools.setup(
    name="uiperf3",
    version="0.1.2",
    author="Damien George",
    author_email="damien.p.george@gmail.com",
    description="Pure Python, iperf3-compatible network performance test tool.",
    long_description="This is a pure Python implementation of a network performance testing tool that is compatible with the popular iperf3 tool.  It runs under Python and MicroPython.",
    url="https://micropython.org",
    py_modules=['uiperf3'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
