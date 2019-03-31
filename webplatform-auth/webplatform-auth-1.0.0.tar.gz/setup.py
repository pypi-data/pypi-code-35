from setuptools import setup, find_packages

setup(name = "webplatform-auth",
   version = "1.0.0",
   description = "Authentication for webplatform",
   author = "Matthew Owens",
   author_email = "mowens@redhat.com",
   url = "https://github.com/lost-osiris/webplatform-auth",
   packages = find_packages(),
   include_package_data = True,
   install_requires = [
      'webplatform-cli',
   ],
   python_requires='>=3',
   license='MIT',
   long_description = """TODO""",
   classifiers = [
       "Programming Language :: Python :: 3",
       "License :: OSI Approved :: MIT License",
       "Operating System :: OS Independent",
   ],
)
