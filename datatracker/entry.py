#!/usr/bin/env python3

import os
import sys
from logzero import logger
import time
from datetime import date
import subprocess

from .file import InputFile, OutputFile

class Entry():
    def __init__(self, tag, description, category, module, version=None):
        self.properties = {
            'tag': tag,
            'description': description,
            'category': category,
            'module': module,
            'version': self.get_version() if not version else str(version),
            'path': __file__ if 'FILE' not in os.environ else os.environ['FILE'],
            'date': str(date.today()),
            'time': time.time(),
            'input_files': [],
            'output_files': []
        }
        self['tag_version'] = f"{self['tag']}_{self['version']}"
        extension = os.path.splitext(self['path'])[1]

    def get_version(self):
        if 'VERSION' in os.environ:
            version = os.environ['VERSION']
        else:
            version = subprocess.run(['git', 'describe'], capture_output=True).stdout.strip().decode()
        return(version)

    def add(self, file):
        if isinstance(file, OutputFile):
            if file['tag'] == 'Artifact':
                file['tag'] = f"Artifact_{len(self['output_files'])}"
                file['description'] = f"{file['description']} ({len(self['output_files'])})"
            self['output_files'].append(file.properties)
        elif isinstance(file, InputFile):
            self['input_files'].append(file.properties)
        else:
            print('File not in the correct format.')
        return(file['path'])

    def show(self):
        return(self.properties)

    def __getitem__(self, property):
        return(self.properties[property])

    def __setitem__(self, index, value):
        self.properties[index] = value

    def __repr__(self):
        return(str(self.properties))

    def __str__(self):
        return(str(self.properties))

    @property
    def dict(self):
        return(self.properties)