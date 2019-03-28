import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='vmi',
    version='0.0.3',
    author='sjtu_6547',
    author_email='88172828@qq.com',
    description='Visual Medical Innovation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://anaconda.org/sjtu_6547/vmi',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Multimedia :: Graphics :: 3D Modeling',
        'Topic :: Multimedia :: Graphics :: 3D Rendering',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
    keywords='PySide2 SimpleITK vtk',
    python_requires='>=3.6',
    install_requires=['PySide2', 'SimpleITK', 'vtk'],
)