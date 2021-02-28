"""
Experiment logging utilities for Machine Learning.
"""

from microlog.internals import experiment


__all__ = [
    'add_pytorch_model',
]


def add_metric(metric_name, value):
    experiment.add_extra_key('metric:' + metric_name, value)


def add_pytorch_model(model):
    pass # TODO
