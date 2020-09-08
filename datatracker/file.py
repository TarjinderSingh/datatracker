#!/usr/bin/env python3

import os
import sys
from datetime import date
import subprocess
from logzero import logger

def is_cloud_path(path):
    return(path[0:3] == 'gs:')

def cloud_path_exists(path):
    return(subprocess.run([ 'gsutil', 'ls', path ], capture_output=True).stderr.decode() is '')

def local_path_exists(path):
    return(os.path.exists(os.path.realpath(os.path.expanduser(path))))

def path_exists(path):
    if is_cloud_path(path):
        return(cloud_path_exists(path))
    else:
        return(local_path_exists(path))

class File():
    def __init__(self, tag, path, description, source=None):
        self.properties = {
                'tag': tag,
                'path': path,
                'description': description,
                'source': source
        }

    def impute_source(self):
        source = 'cloud' if is_cloud_path(self['path']) else 'local'
        return(source)

    def all(self):
        return(self.properties)

    def __getitem__(self, property):
        return(self.properties[property])
    
    def __setitem__(self, index, value):
        self.properties[index] = value

class InputFile(File):
    def __init__(self, **kwargs):
        init_dict = { p: kwargs.get(p, None) for p in [ 'path', 'description', 'source' ] }
        init_dict['tag'] = kwargs['tag']
        super(InputFile, self).__init__(**init_dict)
        self['entry_tag'] = kwargs.get('entry_tag', None)
        self['version'] = kwargs.get('version', None)
        tracker = kwargs.get('database', None)
        #if tracker is None and 'tr' in globals():
        #    tracker = globals()['tr']
        #print(globals())
        #self.tracker = tracker
        #sum([ self[p] is not None for p in ['entry_tag'] ]) == 3 # , 'version', 'database'
        infer_boolean = (int(tracker is not None) + int(self['entry_tag'] is not None)) == 2
        defined_boolean = sum([ self[p] is not None for p in ['path', 'description'] ]) == 2
        if not infer_boolean and not defined_boolean:
            raise('User must provide either the entry_tag, version, and database reference OR path and description.')

        if infer_boolean:
            self.__infer_file_properties(tracker)

        self['exists'] = path_exists(self['path'])
        
    def __infer_file_properties(self, tracker):
        entry = tracker.get_entry(self['entry_tag'], self['version'])
        file = tracker.get_file(self['entry_tag'], self['tag'], self['version'])
        self['version'] = entry['version']
        self['path'] = file['path']
        self['description'] = file['description']
        self['date'] = file['date']

class OutputFile(File):
    def __init__(self, **kwargs):
        init_dict = { p: kwargs.get(p, None) for p in [ 'tag', 'description', 'source' ] }
        init_dict['path'] = kwargs['path']
        super(OutputFile, self).__init__(**kwargs)
        self['date'] = str(date.today())
        self['source'] = self.impute_source() if self['source'] is None else self['source']
        if self['tag'] is None:
            self['tag'] = 'Artifact'
            self['description'] = 'Data artifact.'