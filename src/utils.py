"""
Experiment logging utilities.
"""

from src.internals import experiment
import os
import sys


__all__ = [
    'add_output_file',
    'add_extra',
    'expath',
    'add_pytorch_model',
]


def add_output_file(path):
    experiment.add_output_file(path)


def add_extra(key, value):
    experiment.add_extra_key(key, value)


def expath(path):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(path)

    path = os.abspath(path)

    add_output_file(path)

    return path


def add_pytorch_model(model):
    pass # TODO
