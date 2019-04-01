import setuptools

with open("README.md", "r") as fh:
        long_description = fh.read()

        setuptools.setup(
                name="MagiSlack",
                version="0.1.1",
                author="Lee, Suho",
                author_email="riemannulus@hitagi.moe",
                description="For a make easy and quick command-respond chat bot",
                long_description=long_description,
                long_description_content_type="text/markdown",
                url="https://github.com/riemannulus/MagiSlack",
                packages=setuptools.find_packages(),
                install_requires=[
                        'slackclient',
                ],
                classifiers=[
                            "Programming Language :: Python :: 3.7",
                            "License :: OSI Approved :: MIT License",
                            "Operating System :: OS Independent",
                        ],
        )
