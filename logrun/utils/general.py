"""
General experiment logging utilities.
"""

from typing import Any
from pathlib import Path
import os
from logrun.internals import experiment
from logrun.internals import ensure_dir_exists as _ensure_dir_exists


__all__ = [
    'log_input_file',
    'log_output_file',
    'log_extra',
    'inpath',
    'outpath',
]


def log_input_file(path: str) -> None:
    """
    Add a given input file to be logged.
    """

    if not isinstance(path, (str, Path)):
        raise TypeError("path must be either 'str' or 'pathlib.Path'")

    experiment.add_input_file(path)


def log_output_file(path: str) -> None:
    """
    Add a given output file to be logged.
    """

    if not isinstance(path, (str, Path)):
        raise TypeError("path must be either 'str' or 'pathlib.Path'")

    experiment.add_output_file(path)


def log_extra(value: Any, key: str) -> None:
    """
    Add some additional data given by `value` under key `key`.
    """

    if not isinstance(key, str):
        raise TypeError("key must be 'str'")

    experiment.add_extra_key(key, value)


def inpath(path: str) -> str:
    """
    Add a given input path `path` to be logged, and return it.
    """

    if not isinstance(path, (str, Path)):
        raise TypeError("path must be either 'str' or 'pathlib.Path'")

    path = os.path.abspath(path)

    log_input_file(path)

    return path


def outpath(path: str, ensure_dir_exists: bool = True) -> str:
    """
    Add a given output path `path` to be logged, create its containing directory if it does not
    exist, and return it.
    """

    if not isinstance(path, (str, Path)):
        raise TypeError("path must be either 'str' or 'pathlib.Path'")

    path = os.path.abspath(path)

    if ensure_dir_exists:
        _ensure_dir_exists(path)

    log_output_file(path)

    return path
