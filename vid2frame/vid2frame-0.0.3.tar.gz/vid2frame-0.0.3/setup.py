from setuptools import setup, find_packages

setup(
	name='vid2frame',
	packages=find_packages(),
	description='Video-to-Frames converter',
	version='0.0.3',
	url='https://github.com/dennis199441/vid2frame',
	author='Dennis Cheung',
	author_email='dennis199441@gmail.com',
	install_requires=[
		'opencv-python',
		'numpy'
    ],
	keywords=['pip','dennis','vid2frame']
)