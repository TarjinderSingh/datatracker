#!/usr/bin/env python3

import os
import sys
from logzero import logger
import re
import subprocess
import pandas as pd
from pkg_resources import parse_version


def gsutil(*args, silent=True, debug=False):
    cmd = ['gsutil']
    if debug:
        print(args)
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


def gs_rm(path, recursive=True, silent=True):
    args = ['-m', 'rm']
    if recursive:
        args.append('-r')
    args.append(path)
    output = gsutil(*args, silent=silent)
    return(output)


def gs_mirror(path, dest_bucket, recursive=True, silent=True, debug=False):
    """Mirror nested directories in one bucket to another.

    Parameters
    ----------
    path : str
        Full path to a local directory or Cloud bucket
    dest_bucket : str
        Full path to Cloud bucket
    recursive : bool, optional
        Recursively copy files from the source directory, by default True
    silent : bool, optional
        Print errors or log file from gsutil, by default True
    debug : bool, optional
        Print arguments from the gsutil command, by default False

    Examples
    --------
    >>> gs_mirror('gs://super-psychosis/data/resources/1.0_hl_log-resources',  'gs://superpheno/', silent=False, debug=True)
    """
    args = ['-m', 'cp']
    if recursive:
        args.append('-r')
    args.append(path)
    args.append(os.path.join(dest_bucket, re.search('gs\:\/\/.*?\/(.*)', path).group(1)))
    output = gsutil(*args, silent=silent, debug=debug)
    return(output)


def gs_view(cloudir):
    subprocess.call(
        ['open', 'https://console.cloud.google.com/storage/browser/' + re.sub('gs://', '', cloudir)])


def sync_down(cloudir, localdir, ext='log', flag=''):
    subprocess.call(['mkdir', '-p', localdir])
    cmd = ['gsutil', '-m', 'cp',
           f'-r{flag}',
           f'{cloudir}/*.{ext}',
           localdir]
    p = subprocess.run(cmd, capture_output=True)
    output, error = p.stdout.decode().strip(), p.stderr.decode().strip()
    return(error)


def copy_resources_local(infile, outfile, run=True):
    """Copy file paths locally between two directories on your machine.

    Parameters
    ----------
    infile : str
        source file path
    outfile : str
        output file path
    run : bool, optional
        actually run or dry run, by default True

    Examples
    --------
    >>> relpath = relpath(os.path.join(localdir, 'gnomad.v2.1.1.lof_metrics.by_gene.tsv'))
    >>> copy_resources_local(infile, here(relpath, local=True))
    """
    
    if run:
        os.makedirs(os.path.dirname(outfile), exist_ok=True)
        p = subprocess.run(['cp', infile, outfile], capture_output=True)
        output, error = p.stdout.decode().strip(), p.stderr.decode().strip()
        print(output, error)


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


def submit_dataproc(cluster_name : str, script_path : str, pyfiles_list : list, silent : bool = False, **kwargs):
    """Submit job to Google dataproc cluster

    Parameters
    ----------
    cluster_name : str
        Name of Google dataproc cluster
    script_path : str
        Path to script to be submitted
    pyfiles_list : List[str]
        A list of directories to be zipped and loaded onto cluster
    silent : bool, optional
        Print string if True, by default False

    Examples
    --------
    >>> submit_dataproc(
            cluster_name='cluster04',
            script_path='case-control.py',
            py_files_list=[here('ukbexomes'), '/hlscore/hlscore'],
            silent=False,
            outfile=outfile)
    """

    cmd = f"hailctl dataproc submit {cluster_name} {script_path}"
    cmd += f" --pyfiles={','.join(pyfiles_list)}"
    if kwargs:
        cmd += "".join([ f" --{k} {v}" for k, v in kwargs.items() ])
    if silent:
        logger.info(f'Dataproc submit command: {cmd}')
    else:
        os.system(cmd)
