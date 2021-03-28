#!/usr/bin/env python3

from setuptools import setup, find_packages
import versioneer

with open('README.md') as f:
    readme = f.read()

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
    long_description_content_type='text/markdown',
    author='TarjinderSingh',
    author_email='tsingh@broadinstitute.org',
    url='https://github.com/TarjinderSingh/datatracker',
    license='MIT',
    python_requires='>=3.7',
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=dependencies
)
