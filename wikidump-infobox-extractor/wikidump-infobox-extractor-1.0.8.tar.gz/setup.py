from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import check_call
import requests


with open("README.md", "r") as fh:
    long_description = fh.read()


# https://github.com/nsadawi/Download-Large-File-From-Google-Drive-Using-Python
def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    # https://stackoverflow.com/a/36902139/6942666

    def run(self):
        # Downloads supreme court cases and downloads Google word2vec model
        check_call("git clone https://github.com/EricWiener/supreme-court-cases".split())
        download_file_from_google_drive("0B7XkCwpI5KDYNlNUTTlSS21pQmM", "./GoogleNews-vectors-negative300.bin")
        install.run(self)


setup(
    name="wikidump-infobox-extractor",
    version="1.0.8",
    author="Eric Wiener",
    author_email="ericwiener3@gmail.com",
    description="Wikidump infobox extractor.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EricWiener/wikidump-infobox-extractor",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["infodump"],
    entry_points={
        'console_scripts': ['infodump=infodump.command_line:main'],
    },
    cmdclass={
        'install': PostInstallCommand,
    }
)
