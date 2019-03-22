"""
Setup
KatFetch installer
By Kat Hamer
"""

from setuptools import setup, find_packages


def main():
    """Main function"""
    setup(
        name="KatFetch",
        version="1.2.2",
        entry_points = {
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
