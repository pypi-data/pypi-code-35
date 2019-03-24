from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='git-annex-gui',
    version='0.2.2',
    packages=['gitannexgui'],
    install_requires=[
        "PySide2",
    ],
    extras_require={
        "dev": [
            "twine",
            "invoke",
            "python-language-server",
        ]
    },
    entry_points={
        "console_scripts": [
            "git-annex-gui = gitannexgui.app:main"
        ]
    },
    author='Øystein S. Haaland',
    author_email='oystein.s.haaland@gmail.com',
    description="A small systray app for git annex assistant.",
    long_description=readme(),
    url="https://gitlab.com/joystein/git-annex-gui",
)
