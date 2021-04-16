# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='saltpay_python',
    version='0.1.0',
    description='SDK for Saltpay payments',
    long_description=readme,
    author='Sævar Öfjörð Magnússon, Overcast Software',
    author_email='opensource@overcast.is',
    url='https://github.com/overcastsoftware/python-saltpay',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        'zeep',
    ]
)

