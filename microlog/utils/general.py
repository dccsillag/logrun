"""
General experiment logging utilities.
"""

from microlog.internals import experiment
from microlog.internals import ensure_dir_exists as _ensure_dir_exists
import os
import sys


__all__ = [
    'add_input_file',
    'add_output_file',
    'add_extra',
    'inpath',
    'outpath',
]


def add_input_file(path):
    experiment.add_input_file(path)


def add_output_file(path):
    experiment.add_output_file(path)


def add_input_file(path):
    experiment.add_input_file(path)


def add_extra(key, value):
    experiment.add_extra_key(key, value)


def inpath(path):
    path = os.path.abspath(path)

    add_input_file(path)

    return path


def outpath(path, ensure_dir_exists=True):
    path = os.path.abspath(path)

    if ensure_dir_exists:
        _ensure_dir_exists(path)

    add_output_file(path)

    return path
