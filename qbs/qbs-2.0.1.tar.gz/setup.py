import setuptools

setuptools.setup(
    name="qbs",
    version="2.0.1",
    author="Nonny Moose",
    author_email="moosenonny10@gmail.com",
    description="Quick (and dirty) build system",
    long_description="See the [GitLab repository](https://gitlab.com/"
                     "nonnymoose/qbs) for the most up-to-date documentation."
                     "\n\nNew in version 2.0.0: t_auto command! "
                     "Any existing commands named t_auto will be broken.",
    long_description_content_type="text/markdown",
    url="https://gitlab.com/nonnymoose/qbs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Environment :: Console",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Build Tools",
    ],
    python_requires=">=3",
    entry_points={
        "console_scripts": [
            "qbs = qbs:main"
        ]
    },
    package_data={"qbs": ["conf/default_config.json"]},
    include_package_data=True
)
