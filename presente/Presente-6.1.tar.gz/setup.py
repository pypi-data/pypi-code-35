from setuptools import setup, find_packages

setup(name="Presente",  # Nombre
    version="6.1",  # Versión de desarrollo
    description="Paquete de prueba",  # Descripción del funcionamiento
    author="Bravo India Tango",  # Nombre del autor
    author_email='bravo.india.tango2019@gmail.com',  # Email del autor
    license="GPL",  # Licencia: MIT, GPL, GPL 2.0...
    packages=['Presente'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Education :: Computer Aided Instruction (CAI)",
        "License :: Free For Educational Use",
        "Intended Audience :: Education",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.7",
        "Natural Language :: Spanish"
    ],
    install_requires=[i.strip() for i in open("requirements.txt").readlines()]
)