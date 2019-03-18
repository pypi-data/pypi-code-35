import setuptools

fn = open("README.md", "r", encoding="UTF8")
long_description = fn.read()
fn.close()

setuptools.setup(
    name="PYWDEIMS101",
    version="1.0.1",
    author="Tom Chen",
    author_email="tom.chenyong@qq.com",
    description="WDEIMS组件",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.dev.tencent.com/Tom_Chenyong/WDEIMS101.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
