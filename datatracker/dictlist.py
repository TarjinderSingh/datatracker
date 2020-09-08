
#!/usr/bin/env python3

import os
import sys
from logzero import logger

class DictList():
    def __init__(self, dict_list):
        self.dli = dict_list

    def filter(self, key=None, value=None, cond=None):
        if cond is None:
            cond = lambda item: item[key] == value
        return([item for item in self.dli if cond(item)])

    def filter_first(self, key=None, value=None, cond=None):
        if cond is None:
            cond = lambda item: item[key] == value
        return(next((item for item in self.dli if cond(item)), None))

    def filter_first_index(self, key, value, cond=None):
        if cond is None:
            cond = lambda item: item[key] == value
        return(next((i for i, item in enumerate(self.dli) if cond(item)), None))

    def keys(self):
        return(set([key for item in self.dli for key in item]))

    def values(self, key):
        return(set([item[key] for item in self.dli ]))
    
    def __getitem__(self, key):
        if isinstance(key, int):
            return(self.dli[key])
        else:
            return([item[key] for item in self.dli])

    def __len__(self):
        return(len(self.dli))

    def __str__(self):
        return(str(self.dli))

    def __iter__(self):
        return(self.dli)