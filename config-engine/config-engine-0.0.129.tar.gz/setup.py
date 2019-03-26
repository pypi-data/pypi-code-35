import os
from setuptools import find_packages, setup

BASE = os.path.dirname(__file__)

setup(
    name='config-engine',
    version=open(os.path.join(BASE, 'version')).read().strip(),
    description='Zipari Config Engine',
    url='http://gitlab.zipari.net/cx/config-engine/',
    author='Zipari',
    packages=find_packages(exclude=['test']),
    install_requires=[
        'boto3==1.7.4',
        'Django==2.0.3',
        'django-cors-headers==2.1.0',
        'djangorestframework==3.7.7',
        'djangorestframework-csv==2.1.0',
        'django-filter==1.1.0',
        'django-redis==4.8.0',
        'django-storages==1.6.5',
        'djangorestframework==3.7.7',
        'django-celery-results==1.0.1',
        'psycopg2==2.7.3.2',
        'Faker==0.8.7',
        'fdfgen==0.16.0',
        'openpyxl==2.5.3',
        'psycopg2==2.7.3.2',
        'PyYAML==3.12',
        'raven==6.7.0',
        'redis-py-cluster==1.3.4',
        'pika>=0.12.0',
        'celery>=4.1.0',
        'flower==0.9.2',
        'django-rest-swagger>=2.0.0',
        'drf-yasg==1.11.0',
        'rx==1.6.1',
        'django-simple-history==2.7.0'
    ],
)
