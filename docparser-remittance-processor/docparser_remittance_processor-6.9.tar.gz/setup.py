import setuptools

setuptools.setup(
    name="docparser_remittance_processor",
    version="6.9",
    author="Hudge",
    author_email="",
    description="",
    long_description="",
    long_description_content_type="text/markdown",
    url="",
    py_modules=["docparser_remittance_processor"],
    install_requires=[
        "xlrd",
        "money2float",
        "semi_structured_text_extractor",
        "split_alphanumeric",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
