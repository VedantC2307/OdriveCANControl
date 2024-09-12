from setuptools import find_packages
from setuptools import setup

setup(
    name='data_sync',
    version='0.0.0',
    packages=find_packages(
        include=('data_sync', 'data_sync.*')),
)
