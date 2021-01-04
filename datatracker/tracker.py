#!/usr/bin/env python3

import os
import sys
import pandas as pd
import subprocess
from shutil import copyfile
from collections import Counter
from logzero import logger
from tinydb import TinyDB, Query
from .dictlist import DictList
from .utils import sort_versions


class Tracker(object):
    def __init__(self, path=None):
        """Constructor for class Tracker"""
        self.path = path if path is not None else os.environ['TRACKER_PATH']
        self.db = TinyDB(self.path)
        self.entry = Query()

    def save(self, entry):
        self.db.insert(entry.properties)
        self.deduplicate()
        self.label_recent()

    def filter(self, cond):
        """tr.filter(tr.entry.tag == "tag")"""
        return(self.db.search(cond))

    def uniq(self, property):
        return(set(self[property]))

    def label_recent(self):
        tags = self.uniq('tag')
        for t in tags:
            entries = self.filter(self.entry.tag == t)
            versions = [e['version'] for e in entries]
            most_recent = sort_versions(versions)[-1]
            self.db.update({'most_recent': True}, ((
                self.entry.tag == t) & (self.entry.version == most_recent)))
            self.db.update({'most_recent': False}, ((
                self.entry.tag == t) & (self.entry.version != most_recent)))

    def remove(self, cond):
        """tr.remove(tr.entry.tag == "tag")"""
        logger.info(f"Conditional for removing entries: {cond}")
        self.db.remove(cond)

    def deduplicate(self):
        vtags = [key for key, value in Counter(
            self['tag_version']).items() if value >= 2]
        for tv in vtags:
            entries = self.filter(self.entry.tag_version == tv)
            times = [e['time'] for e in entries]
            most_recent = sorted(times)[-1]
            self.db.remove(((self.entry.tag_version == tv) &
                            (self.entry.time != most_recent)))

    def copy(self, path):
        copyfile(self.path, path)
        return(Tracker(path))

    def get_entry(self, entry_tag, version=None):
        if version is not None:
            entry = self.filter((self.entry.tag == entry_tag) & (
                self.entry.version == version))[0]
        else:
            entry = self.filter((self.entry.tag == entry_tag) & (
                self.entry.most_recent == True))[0]
        return(entry)

    def get_file(self, entry_tag, file_tag, version=None):
        """Get File dictionary given entry tag and file tag

        Parameters
        ----------
        entry_tag : str
            Entry tag in database
        file_tag : str
            File tag identifying specific file
        version : str, optional
            Version string if not going by most recent, by default None

        See Also
        --------
        get_entry, get_file_path

        Examples
        --------
        >>>tr.get_file("entry_tag", "file_tag")
        """
        entry = self.get_entry(entry_tag, version)['output_files']
        dli = DictList(entry)
        return(dli.filter_first(cond=lambda x: x['tag'] == file_tag))

    def get_file_path(self, *args, **kwargs):
        return(self.get_file(*args, **kwargs)['path'])

    def get_output_files(self, entry_tag, version=None):
        """Get list of output files from an entry.

        Parameters
        ----------
        entry_tag : str
            Entry tag in database
        version : str, optional
            Version string if not going by most recent, by default None

        See Also
        --------
        get_entry

        Examples
        --------
        >>>tr.get_output_files("entry_tag")
        """
        return(self.get_entry(entry_tag, version)['output_files'])

    def update(self):
        pass

    def to_pandas(self, tag=None, module=None, most_recent=True):
        df = pd.DataFrame.from_dict([row for row in self.db])
        if df.empty:
            return(df)
        df = df.sort_values('time', ascending=False)
        if tag:
            df = df[df.tag == tag]
        if module:
            df = df[df.module == module]
        if most_recent:
            df = df[df.most_recent]
        return(df)

    def explode(self, *args, **kwargs):
        df = self.to_pandas(*args, **kwargs)

        df = df[['tag', 'category', 'module', 'description',
                 'version', 'input_files', 'output_files', 'most_recent', 'time']]

        df0 = df.drop('output_files', axis=1).rename(
            {'input_files': 'files'}, axis=1)
        df1 = df.drop('input_files', axis=1).rename(
            {'output_files': 'files'}, axis=1)

        df0 = self._explode_files(df0)
        df1 = self._explode_files(df1)

        df = pd.concat([df0.assign(type='input'),
                        df1.assign(type='output')], axis=0)
        df['basename'] = df['path'].apply(os.path.basename)
        df = df[['tag', 'category', 'module', 'file_tag', 'description', 'type',
                 'file_desc', 'basename', 'path', 'most_recent', 'index', 'time']]
        df = df.sort_values(['time', 'category', 'module', 'tag', 'type', 'index'], ascending=[
                            False, True, True, True, True, True])
        return(df)

    def _explode_files(self, df):
        df['files'] = df['files'].map(
            lambda l: [dict(x, **{'index': i}) for i, x in enumerate(l)])
        df = df.explode('files')
        df = df[df.files.notnull()]
        df['file_tag'] = df['files'].map(lambda x: x['tag'])
        df['path'] = df['files'].map(lambda x: x['path'])
        df['file_desc'] = df['files'].map(lambda x: x['description'])
        df['index'] = df['files'].map(lambda x: x['index'])
        df = df.drop('files', axis=1)
        return(df)

    def to_excel(self, path, **kwargs):
        df = self.to_pandas(**kwargs)
        df.to_excel(path)

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
        return(self.to_pandas(tag=None, most_recent=False))

    @property
    def summary(self):
        df = self.table[['category', 'module', 'tag', 'description',
                         'version', 'date', 'time', 'most_recent']]
        return(df.sort_values('time', ascending=False))
