import setuptools

import fidget

setuptools.setup(
    name=fidget.__name__,
    version=fidget.__version__,
    author=fidget.__author__,
    url=r'https://github.com/talos-gis/Fidget',
    packages=['fidget', 'fidget.widgets', 'fidget.backend'],
    extras_require={
        'PyQt': ['PyQt5'],
        'PySide': ['PySide2']
    },
    python_requires='>=3.7.0',
    include_package_data=True,
    data_files=[
        ('', ['README.md', 'CHANGELOG.md']),
    ],
)
