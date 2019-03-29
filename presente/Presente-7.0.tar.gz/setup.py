from setuptools import setup, find_packages

setup(name="Presente",  # Nombre
    version="7.0",  # Versión de desarrollo
    description="Programa para listar presente en clase",  # Descripción del funcionamiento
    author="Bravo India Tango",  # Nombre del autor
    author_email='bravo.india.tango2019@gmail.com',  # Email del autor
    license="GPL",  # Licencia: MIT, GPL, GPL 2.0...
    packages=['Presente'],
    keywords = ['school', 'QR', 'PDF'],
    classifiers=[
        
        "Topic :: Education :: Computer Aided Instruction (CAI)",
        "License :: Free For Educational Use",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3.7",
        "Natural Language :: Spanish"
    ],
    install_requires=[i.strip() for i in open("requirements.txt").readlines()]
)