"""
Setup
KatFetch installer
By Kat Hamer
"""

from setuptools import setup, find_packages

with open("README.md", "r") as fp:
    long_description = fp.read()


def main():
    """Main function"""
    setup(
        name="KatFetch",
        version="1.2.1",
        author="Katelyn Hamer",
        description="Minimal and customizable fetch script written in Python3 <3",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://gitlab.com/kathamer/katfetch",
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
        ],

        entry_points={
                      "console_scripts": [
                          "katfetch = katfetch:main"
                      ]
        },
        install_requires=["distro",
                          "py-cpuinfo",
                          "hurry.filesize",
                          "psutil",
                          "click"],
        packages=find_packages()
    )


if __name__ == "__main__":
    main()  # Run main function
