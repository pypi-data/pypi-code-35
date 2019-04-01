from setuptools import setup

setup(
    name="lambdapy",
    author="Jacob Jäger",
    maintainer="Jacob Jäger",
    version="0.0.2",
    description="Untyped Lambda calculus in python",
    py_modules=['lambdapy', 'lambdapy.core', 'lambdapy.repl'],
    install_requires=["tatsu"],
    entry_points={
        'console_scripts': [
            "lambda=lambdapy.repl:repl"
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
    ]
)