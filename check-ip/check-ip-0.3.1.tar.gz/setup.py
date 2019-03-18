from setuptools import setup

with open("README.md") as f:
    README = f.read()

setup(
    name="check-ip",
    version="0.3.1",
    description="Check your public IP address and update DNS records on Cloudflare.",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Samuel Searles-Bryant",
    author_email="devel@samueljsb.co.uk",
    license="MIT",
    url="https://github.com/samueljsb/check-ip/",
    py_modules=["check_ip"],
    install_requires=["requests", "click", "pyyaml"],
    entry_points={"console_scripts": ["check-ip=check_ip:main"]},
)
