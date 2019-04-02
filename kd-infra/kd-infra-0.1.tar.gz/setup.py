'''
Created on 20190328
@auther: dq
'''
from setuptools import setup,find_packages
setup(name = 'kd-infra',
      version= '0.1',
      keywords = ('pip', 'infra', 'featureextraction'),
      description = 'Custom script',
      license = 'MIT Licence',
      url = 'https://github.com/duquan640/pip_kd/kd_infra',
      author = 'dq',
      author_email = 'duquan@kuandeng.com',
      packages = find_packages(),
      include_package_data = True,
      platforms = "any"
      #packages = ['kd_infra'],
     )
