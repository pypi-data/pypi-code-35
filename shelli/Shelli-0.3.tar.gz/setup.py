from setuptools import setup

setup(
    name='Shelli',
    version='0.3',
    description=open('README.md').read(),
    url='https://github.com/kindlehl/shelli',
    author='Hunter Lannon',
    author_email='hunter.d.lannon@gmail.com',
    license='GPLv3',
    packages=['shelli'],
    entry_points={
        "console_scripts": ['shelli = shelli.main:main']
    },
    install_requires=[
        'fabric>=2.4.0',
        # Change after this merges https://github.com/paramiko/paramiko/issues/1386
        'cryptography==2.3',
        'PyYAML>=5.1',
    ],
    zip_safe=False,
)
