from setuptools import *

setup(
	name="mixmaster",
	packages=find_packages(),
	version="1.1",
	license="MIT",
	author="Ray Speth, Bryan W. Weber",
	author_email="yarmond@gmail.com, bryan.w.weber@gmail.com",
	url="https://github.com/Cantera/mixmaster",
	description="Mixmaster is a Cantera based GUI that allows you to import reaction mechanisms and to view or set the state of mixtures." \
				  "It can carry out the thermodynamic processes and compute the chemical equilibrium. It gives the data related to reaction and chemical species." \
				  " It postprocess the simulation data ans shows the reaction paths.   ",
	install_requires=[
		"numpy",
		"matplotlib",
	]
)
