from distutils.core import setup
setup(
	name = 'vk_analyse',
	packages = ['vk_analyse'],
	version = '0.2',
	description = 'Get user vk information',
	author = 'Solovey R',
	author_email = 'solovey.roma68@gmail.com',
	url = 'https://github.com/romkasolovey/vk_analyse',
	download_url = 'https://github.com/romkasolovey/vk_analyse/tarball/0.2',
	keywords = ['vk api','louvain','vk'],
	classifiers = [],
	install_requires=["networkx","requests"],
)