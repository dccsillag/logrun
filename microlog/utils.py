"""
Experiment logging utilities.
"""

from microlog.internals import experiment
import os
import sys


__all__ = [
    'add_output_file',
    'add_extra',
    'inpath',
    'expath',
    'add_pytorch_model',
]


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


def expath(path):
    path = os.path.abspath(path)

    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    add_output_file(path)

    return path


def add_pytorch_model(model):
    pass # TODO
