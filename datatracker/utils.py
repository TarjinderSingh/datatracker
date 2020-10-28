#!/usr/bin/env python3

import os
import sys
from logzero import logger
import subprocess

def gsutil(*args, silent=False):
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
