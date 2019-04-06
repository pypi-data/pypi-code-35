from setuptools import setup


setup(name='cryptiles',
      version='0.1',
      license='BSD2CLAUSE',
      install_requires=['pycrypto'],
      packages=['cryptiles'],
      package_data={'cryptiles': ['cryptiles/*']},
      data_files=[('LICENSE')],
      entry_points={'console_scripts': ['cryptile=cryptiles.__main__:main']},
      description='A simple script to encrypt and decrypt data.',
      long_description=("Cryptiles use XOR and a passkey to encrypt and decrypt a string data  "
                        "or file content passed like arguments in the cmd line."),
      author='Silvio Ap Silva a.k.a Kanazuchi',
      author_email='contato@kanazuchi.com',
      url='http://github.com/kanazux/cryptiles',
      zip_safe=False)