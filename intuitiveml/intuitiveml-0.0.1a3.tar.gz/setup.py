from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='intuitiveml',
      version='0.0.1a3',
      install_requires=['numpy', 'scipy', 'pandas', 'scikit-learn', 'plotly', 'ipywidgets', 'deepreplay'],
      description='Intuitive ML',
      long_description=readme(),
      long_description_content_type='text/markdown',
      url='',
      author='Daniel Voigt Godoy',
      author_email='datagnosis@gmail.com',
      keywords=['machine learning', 'algorithms', 'visualization', 'interactive'],
      license='MIT',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
          'Topic :: Scientific/Engineering :: Visualization',
          'Topic :: System :: Distributed Computing',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3'
      ],
      packages=find_packages(),
      zip_safe=False)

