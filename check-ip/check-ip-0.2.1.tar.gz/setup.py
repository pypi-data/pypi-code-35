from setuptools import setup

with open("README.rst") as f:
    README = f.read()

setup(
    name="check-ip",
    version="0.2.1",
    description="Check your public IP address and update DNS records on Cloudflare.",
    long_description=README,
    author="Samuel Searles-Bryant",
    author_email="devel@samueljsb.co.uk",
    license="MIT",
    url="https://github.com/samueljsb/check-ip/",
    py_modules=["check_ip"],
    install_requires=["requests", "loguru", "pyyaml"],
    entry_points={"console_scripts": ["check-ip=check_ip:main"]},
)
