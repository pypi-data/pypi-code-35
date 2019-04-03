from setuptools import setup

setup(name='mgl_efis_plotter',
      version='0.1.1',
      description='MGL EFIS data plotter',
      long_description='Plot and export flight data from the MGL iEFIS systems',
      classifiers=[
          'Programming Language :: Python :: 3.6',
      ],
      url='https://github.com/azemon/mgl_efis_plotter',
      author='Art Zemon',
      author_email='art@zemon.name',
      license='MIT',
      packages=['mgl_efis_plotter'],
      install_requires=['matplotlib', 'pandas'],
      zip_safe=False
)
