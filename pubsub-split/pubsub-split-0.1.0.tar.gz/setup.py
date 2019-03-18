from setuptools import setup, find_packages


setup(
    name="pubsub-split",
    version="0.1.0",
    description=(
        """GCP Pubsub requires messages to be less than a certain size. This library
        splits collections of items to ensure that limit is not reached.

        Note: Assumes users are commonly sending lists of items, rather than
        large or complex python data types or dictionaries."""
    ),
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="pubsub split",
    author="Jon Robison",
    author_email="narfman0@gmail.com",
    license="LICENSE",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=["google-cloud-pubsub"],
    test_suite="tests",
)
