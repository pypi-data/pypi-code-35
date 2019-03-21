from setuptools import setup,find_packages

setup(
	name = 'ct_tools',
	version = "0.0.3",
	packages = find_packages(),
	include_package_data=True,    
	exclude_package_data={'':['.gitignore']},
	description="personal use",
	author ="Vvegetables",
	url="https://github.com/Vvegetables/ct_tools",
	author_email="hardwork_fight@163.com",
	license="Public domain",
	install_requires=[
		"PyMysql>=0.9.2",
		"Django>=1.11.5",
	],
)