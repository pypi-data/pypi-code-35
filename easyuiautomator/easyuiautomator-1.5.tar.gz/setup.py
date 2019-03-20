try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='easyuiautomator',
    version='1.5',
    platforms='any',
    url='',
    license='MIT',
    author='thomas.ning',
    author_email='ningruhu@163.com',
    description='',
    keywords=('testing', 'android', 'uiautomator'),
    packages=['easyuiautomator', 
              'easyuiautomator.common', 
              'easyuiautomator.driver', 
              'easyuiautomator.driver.common',
              'easyuiautomator.driver.executor'
    ],
    package_data={
        'easyuiautomator': [
            'resource/u1/YepTelecomBootstrap.jar',
            'resource/u2/testguard-uiautomator.apk',
            'resource/u2/testguard-uiautomator-test.apk',
        ],
    },
    data_files=[
                ("Lib/site-packages",
                  ["cv2.pyd"]
                )
    ],
    include_package_data=True,
    install_requires=['requests>=2.18.1'],
    zip_safe=False
)
