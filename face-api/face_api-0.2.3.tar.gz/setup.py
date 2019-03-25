import setuptools
from face_api import __version__, __author__, __email__

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    'numpy',
    'Pillow',
    'grpcio',
    'tensorflow',
    'tensorflow-serving-api',
    'dlib',
    'click'
]

setuptools.setup(
    name="face_api",
    version=__version__,
    author=__author__,
    author_email=__email__,
    description="Package for Face API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://www.ai.game.tw",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'gen_imgs=face_api.gen_imgs:main',
            'ex_img2fes=face_api.ex_img2fes:main',
            'ex_imgs2conf_matrix=face_api.ex_imgs2conf_matrix:main',
            'help_face_api=face_api.helper:main',
        ]
    },    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)
