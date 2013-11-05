# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import sys

if not (sys.version_info[0]== 2 and sys.version_info[1] == 7):
    print "Sorry, only python 2.7.x is supported for mosaic"
    sys.exit(1)


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='mosaic',
    version='0.0.1',
    description="Create images similar to Delta909's Pixel Matrix on arbitrary pictures",
    long_description=readme,
    author='Indraniel Das',
    author_email='indraniel@gmail.com',
    url='https://github.com/indraniel/tinted-mosaic',
    license=license,
    scripts=['bin/pixel-art'],
    install_requires=['nose==1.3.0','Pillow==2.2.1'],
    packages=find_packages(exclude=('tests', 'docs')),
    package_data={ '': ['*.md', 'LICENSE'], },
    include_package_data=True
)
