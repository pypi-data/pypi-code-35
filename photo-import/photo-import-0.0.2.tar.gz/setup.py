import re

from setuptools import setup

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('photoimport/__init__.py').read(),
    re.M
).group(1)

with open("README.md", "rb") as f:
    readme = f.read().decode("utf-8")

setup(
    name="photo-import",
    packages=["photoimport"],
    entry_points={
        "console_scripts": ['photo-import = photoimport.command:main']
    },
    version=version,
    description="Application to import photos into a hierarchical structure based on the EXIF data of the photos.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Edd Armitage",
    author_email="edward.armitage@gmail.com",
    url="https://gitlab.com/eddarmitage/photo-import",
    license="MIT",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=["exif", "docopt"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pyfakefs"],
    extras_require={
        'python_version<=3.7': ['backports-datetime-fromisoformat==1.0.0', ],
    },
)
