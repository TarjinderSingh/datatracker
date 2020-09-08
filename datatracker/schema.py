#!/usr/bin/env python3

import os
import sys
from logzero import logger

entry_properties = {
    'init': [
        # defines entry group
        'tag',
        'description',
        'category',
        'module'
    ],
    'env': [
        'version',
        'script_path',
        'git_hash',
        'date_rendered',
        'core_libraries', # : [ {'library': '', 'version': '' }]
    ],
    'calc': [
        # unique, calculated from tag and version
        'tag_version',
        # from script name
        'language'
    ],
    'update': [
        # calculated, inverse is 'is_retired'
        'is_current',
        # calculated by date and module
        'order'
    ]
}

input_properties = {
    'init': [
        'tag', # user-defined, unique
        'entry_tag',
        'version', # can be default or most recent
        'path', # optional, search in output_properties
        'description', # optional, search in output_properties
        'source', # optional, search in output_properties, cloud or local
    ],
    'calc': [
        'exists'
    ]
}
output_properties = {
    'init': [
        'tag', # user-defined, unique
        'path',
        'description',
        'source', # optional, search in output_properties, cloud or lcal
    ],
    'calc': [
        'date',
        'exists',
        'source'
    ]
}