import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ComplexTDL",
    version="1.0.0",

    author="Antony Xu",
    author_email="xiaoxu1993ha@126.com",
    description="A complex to do list tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maquedexiju/ComplexTDL",

    packages=setuptools.find_packages(exclude=['.vscode', '.gitignore']),
    include_package_data=True,
    scripts=['td_modify', 'td_report', 'td_set'],
    install_requires=['openpyxl>=2.4.8', 'pyperclip>=1.6.4', 'tinydb>=3.11.1'],

    platforms="any",
    python_requires='>=3'
)