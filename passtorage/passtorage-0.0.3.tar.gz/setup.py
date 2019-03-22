import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="passtorage",
    version="0.0.3",
    requires = ['tkinter', 'random', 'pyperclip'],
    author="Matías Pretz",
    url='https://github.com/Matipretz/passtorage',
    platforms='Win10',
    license= 'MIT',
    entry_points={'gui_scripts': ['passtorage = passtorage.__main__:main'],'console_scripts': ['passtorage-cli = passtorage.__main2__:main']},
    author_email="matipretz@gmail.com",
    description="txt password generator and manager with tkinter.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    packages=['passtorage'],
    classifiers=[
        "Environment :: Win32 (MS Windows)",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Programming Language :: Python :: 3.7",
        "Topic :: Security",
        "Topic :: Utilities"]
    )
