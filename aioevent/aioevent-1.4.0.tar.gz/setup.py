from setuptools import setup, find_packages

setup(
    name="aioevent",
    author="Travis DePrato",
    author_email="travisdeprato@gmail.com",
    version="1.4.0",
    description="Events for asyncio.",
    packages=find_packages("."),
    install_requires=[],
    python_requires=">=3.6",
)
