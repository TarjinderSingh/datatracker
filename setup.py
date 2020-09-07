#!/usr/bin/env python3

from setuptools import setup, find_packages
import versioneer

with open('README.md') as f:
    readme = f.read()

with open('LICENSE.md') as f:
    license = f.read()

dependencies = []
with open('requirements.txt', 'r') as f:
    for line in f:
        dependencies.append(line.strip())

setup(
    name='datatracker',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='Methods to help track the scripts and datafiles in a project.',
    long_description=readme,
    author='TarjinderSingh',
    author_email='',
    url='https://github.com/TarjinderSingh/datatracker',
    license=license,
    python_requires=">=3.7",
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=dependencies
)
