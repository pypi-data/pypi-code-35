"""
Setup
KatFetch installer
By Kat Hamer
"""

from setuptools import setup, find_packages
import katfetch


def long_description():
    """Read README.md"""
    with open("README.md") as fp:
        long_description = fp.read()
    return long_description


def main():
    """Main function"""
    setup(
        name=katfetch.__name__,
        version=katfetch.__version__,
        entry_points={
            "console_scripts": [
                "katfetch = katfetch.__main__:main"
            ]
        },
        install_requires=["distro",
                          "hurry.filesize",
                          "psutil",
                          "click"],
        package_dir={"": "katfetch"},

        author=katfetch.__author__,
        description=katfetch.__description__,
        long_description=long_description(),
        long_description_content_type='text/markdown',
        license=katfetch.__license__,
        keywords=katfetch.__keywords__,
        url=katfetch.__url__,

        classifiers=[
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python',
            'Operating System :: POSIX :: Linux'
        ],
    )


if __name__ == "__main__":
    main()  # Run main function
