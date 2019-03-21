from setuptools import setup

setup(name='pynpflow',
      version='0.2',
      description='Optical flow library for python. ',
      url='https://github.com/JuanFMontesinos/PyOF',
      author='Juan Montesinos',
      author_email='juanfelipe.montesinos@upf.edu',
      packages=['pyflow'],
      install_requires = ['imageio','opencv-python','numpy','matplotlib','scipy','scikit-image'],
      zip_safe=False)
