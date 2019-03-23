from setuptools import setup

with open('README.txt', encoding='UTF-8') as f:
	a=f.read()

setup(
	name='trizio2sce',
	author="Pedro Fernández",
	author_email="rockersuke@gmail.com",
	version='1.0.5b1',
	license="MIT",	
	url="http://www.zonafi.rockersuke.com/trizio2sce/index.html",
	description="Convierte mapas de aventuras de texto generados por Trizbort.io en código fuente para el DAAD.",
	long_description=a,
	python_requires=">=3.5",
	scripts=['trizio2sce.py']
)