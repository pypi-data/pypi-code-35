import setuptools

version = "0.7.0"

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="atlastk",
    version=version,
    author="Claude SIMON",
#    author_email="author@example.com",
    description="A fast and easy way to add sharable web interfaces to Python programs.",
    keywords="web interface",
    license="AGPL-3.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://q37.info/s/c7hfkzvs",
    packages=setuptools.find_packages(),
    project_urls={
    'Contact': 'https://q37.info/s/ggq7x4w7',
    'Homepage': 'http://atlastk.org',
    'Source': 'http://q37.info/s/c7hfkzvs',
    },
    classifiers=[
      "Environment :: Web Environment",
      "Development Status :: 5 - Production/Stable",
      "Intended Audience :: Developers",
      "Intended Audience :: Education",
      "Intended Audience :: Other Audience",
      "License :: OSI Approved :: GNU Affero General Public License v3",
      "Operating System :: OS Independent",
      "Programming Language :: Python :: 2",
      "Programming Language :: Python :: 3",
      "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
      "Topic :: Software Development :: User Interfaces"
    ]
)