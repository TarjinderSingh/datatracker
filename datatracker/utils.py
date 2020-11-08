#!/usr/bin/env python3

import os
import sys
from logzero import logger
import re
import subprocess
import pandas as pd
from pkg_resources import parse_version


def gsutil(*args, silent=True):
    cmd = ['gsutil']
    if len(args) == 1:
        cmd = f'{cmd[0]} {args[0]}'
        shell = True
    else:
        cmd.extend(args)
        shell = False
    p = subprocess.run(cmd, shell=shell, capture_output=True)
    output, error = p.stdout.decode().strip(), p.stderr.decode().strip()
    if not silent:
        log_str = f"{cmd}" if error is b'' else f"{cmd}\n{error}"
        logger.info(log_str)
    return(output)


def gs_ls(path, pattern=None, trimdir=True):
    """gs_ls(tr.get_file_path('rare-gtfilt-genotypes-mt', 'rare-filtered-genotypes-mt'), pattern='.mt$')"""
    output = gsutil(*['ls', path])
    if re.search("\n", output):
        output = output.split("\n")
        if trimdir:
            output = [re.sub('\\/$', '', o) for o in output]
        if pattern:
            output = [o for o in output if re.search(pattern, o)]
        if len(output) == 1:
            output = output[0]
    return(output)


def is_cloud_path(path):
    return(path[0:3] == 'gs:')


def cloud_path_exists(path):
    return(subprocess.run(['gsutil', 'ls', path], capture_output=True).stderr.decode() is '')


def local_path_exists(path):
    return(os.path.exists(os.path.realpath(os.path.expanduser(path))))


def path_exists(path):
    if is_cloud_path(path):
        return(cloud_path_exists(path))
    else:
        return(local_path_exists(path))


def filter_list(arr, pattern):
    arr = [a for a in arr if re.search(pattern, a)]
    if len(arr) == 1:
        return(arr[0])
    else:
        return(arr)


def excel_cache(df, name='summary'):
    """outfile = excel_cache(tr.summary, 'summary'); ! open $outfile"""
    outfile = f'{name}.xlsx'
    df.to_excel(outfile, index=None)
    return(outfile)


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