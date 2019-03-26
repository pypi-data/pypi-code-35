from distutils.core import setup

readme = open('README.md','r')
README_TEXT = readme.read()
readme.close()


setup(
  name = 'dclims',
  packages = ['dclims'], # this must be the same as the name above
  version = '0.4',
  description = 'A simple wrapper for the D.C. Legislative Information Management System (DC LIMS)',
  long_description =  README_TEXT,
  long_description_content_type="text/markdown",
  author = 'Michael Watson',
  author_email = 'michael@dcpolicycenter.org',
  url = 'https://github.com/dc-policy-center/DC-LIMS',
  download_url = 'https://github.com/dc-policy-center/DC-LIMS/archive/0.1.tar.gz',
  keywords = ['wrapper', 'legislation', 'D.C.'],
  classifiers = [],
)
