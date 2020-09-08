#!/usr/bin/env python3

import os
import sys
import pandas as pd
from shutil import copyfile
from collections import Counter
from logzero import logger
from tinydb import TinyDB, Query

from .dictlist import DictList

class Tracker(object):
    def __init__(self, path):
        """Constructor for class Tracker"""
        self.path = path
        self.db = TinyDB(self.path)
        self.entry = Query()

    def add(self, entry):
        self.db.insert(entry.properties)
        #self.deduplicate()
        self.label_recent()

    def filter(self, cond):
        return(self.db.search(cond))

    def uniq(self, property):
        return(set(self[property]))

    def label_recent(self):
        tags = self.uniq('tag')
        for t in tags:
            entries = self.filter(self.entry.tag == t)
            versions = [ e['version'] for e in entries ]
            most_recent = sort_versions(versions)[-1]
            self.db.update({'most_recent': True}, ((self.entry.tag == t) & (self.entry.version == most_recent)))
            self.db.update({'most_recent': False}, ((self.entry.tag == t) & (self.entry.version != most_recent)))

    def deduplicate(self):
        vtags = [ key for key, value in Counter(self['tag_version']).items() if value >= 2 ]
        for tv in vtags:
            entries = self.filter(self.entry.tag_version == tv)
            times = [e['time'] for e in entries]
            most_recent = sorted(times)[-1]
            self.db.remove(((self.entry.tag_version == tv) & (self.entry.time != most_recent)))

    def copy(self, path):
        copyfile(self.path, path)
        return(Tracker(path))

    def find_entry(self, entry_tag, version=None):
        if version is not None:
            entry = self.filter((self.entry.tag == entry_tag) & (self.entry.version == version))[0]
        else:
            entry = self.filter((self.entry.tag == entry_tag) & (self.entry.most_recent == True))[0]
        return(entry)

    def find_file(self, entry_tag, file_tag, version=None):
        dli = self.find_entry(entry_tag, version)['output_files']
        dli = DictList(dli)
        return(dli.filter_first(cond=lambda x: x['tag'] == file_tag))

    def find_file_path(self, *args, **kwargs):
        return(self.find_file(*args, **kwargs)['path'])

    def update(self):
        pass

    def kill(self):
        self.db.truncate()

    def __len__(self):
        return(len(self.db))

    def __getitem__(self, property):
        return([row[property] for row in self.db])

    @property
    def entries(self):
        return(self.db.all())

    @property
    def table(self):
        return(pd.DataFrame.from_dict([ row for row in self.db ]))

from pkg_resources import parse_version
def sort_versions(arr):
    """Sort version tags using pkg_resource definition.

    Parameters
    ----------
    arr : list

    Examples
    --------
    >>> versions = ['0.1', '0.10', '0.2.1', '0.2', '0.10.1',
            '0.1.1+0.g3c5592b.dirty', '0.1.5', '0.2', '0.2']
    >>> sort_versions(versions)
    """
    return(sorted(arr, key=parse_version))