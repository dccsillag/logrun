"""
General experiment logging utilities.
"""

from pathlib import Path
import os
import sys
from microlog.internals import experiment
from microlog.internals import ensure_dir_exists as _ensure_dir_exists


__all__ = [
    'add_input_file',
    'add_output_file',
    'add_extra',
    'inpath',
    'outpath',
]


def add_input_file(path):
    if not isinstance(path, (str, Path)):
        raise TypeError("path must be either 'str' or 'pathlib.Path'")

    experiment.add_input_file(path)


def add_output_file(path):
    if not isinstance(path, (str, Path)):
        raise TypeError("path must be either 'str' or 'pathlib.Path'")

    experiment.add_output_file(path)


def add_extra(key, value):
    if not isinstance(key, str):
        raise TypeError("key must be 'str'")

    experiment.add_extra_key(key, value)


def inpath(path):
    if not isinstance(path, (str, Path)):
        raise TypeError("path must be either 'str' or 'pathlib.Path'")

    path = os.path.abspath(path)

    add_input_file(path)

    return path


def outpath(path, ensure_dir_exists=True):
    if not isinstance(path, (str, Path)):
        raise TypeError("path must be either 'str' or 'pathlib.Path'")

    path = os.path.abspath(path)

    if ensure_dir_exists:
        _ensure_dir_exists(path)

    add_output_file(path)

    return path
