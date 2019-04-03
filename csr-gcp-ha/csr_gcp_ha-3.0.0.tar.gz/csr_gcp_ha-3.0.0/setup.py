from distutils.core import setup
from setuptools.command.install import install
import subprocess


project_name = 'csr_gcp_ha'
project_ver = '3.0.0'


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        print("We are running in the postInstallCommand")
        subprocess.call(['pip', 'install', 'csr_gcp_utils~=1.0', '--user'])
        subprocess.call(['pip', 'install', 'csr_ha~=1.0','--user'])
        install.run(self)


setup(
    name=project_name,
    version=project_ver,
    description='Utilities for csr1000v on GCP',
    author='Avani Vyas',
    author_email='avvyas@cisco.com',
    # use the URL to the github repo
    url='https://github4-chn.cisco.com/csr1000v-gcp/csr_gcp_ha',
    download_url='https://github4-chn.cisco.com/csr1000v-gcp/' + project_name + '/archive/' + \
        project_ver + '.tar.gz',
    keywords=['cisco', 'gcp', 'guestshell', 'csr1000v', 'high availability'],
    classifiers=[],
    license="MIT",
    include_package_data=True,
    cmdclass={
        'install': PostInstallCommand,
    }
)
