import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kafka_splunk_connector",
    version="1.0.6",
    author="Sathish",
    author_email="sathishsathi500@gmail.com",
    description="Library that connects the kafka topic to splunk",
    long_description=long_description,
    install_requires=[
	'kafka-python',
	'requests',
	'logging',
	'splunk_hec_handler'
    ],
    long_description_content_type="text/markdown",
    url="https://github.com/Sathishsathi/kafka_splunk_connector",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
	"Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
	"License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
