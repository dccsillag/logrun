"""
Experiment logging utilities for Machine Learning.
"""

from microlog.internals import experiment


__all__ = [
    'add_pytorch_model',
]


def add_metric(metric_name, value):
    if not isinstance(key, str):
        raise TypeError("key must be 'str'")

    experiment.add_extra_key('metric:' + metric_name, float(value), overwrite=False)


def add_pytorch_model(model):
    pass # TODO
