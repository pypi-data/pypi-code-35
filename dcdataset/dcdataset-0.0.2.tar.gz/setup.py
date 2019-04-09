import setuptools

with open("README.md", "r") as fh:
    for line in fh.readlines():
        if "Version" in line:
            version = line.split(":")[1].strip().rstrip('\n')

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    'urllib3',
]

print("Build: dcdataset")
print(". Version: {}".format(version))
print(". Requirements: {}".format(requirements))

setuptools.setup(
    name="dcdataset",
    version=version,
    author="YL & SW",
    author_email = 'deepcluster.io@gmail.com',
    description="DeepCluster dataset service package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=['*.test', '*.test.*', 'test.*','test']),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)