"""
Experiment logging utilities for Machine Learning.
"""

from logrun.internals import experiment


__all__ = [
    'add_metric',
    'add_pytorch_model',
]


def add_metric(metric_name, value):
    """
    Add a value `value` of a metric identified by `metric_name` to the extra keys to be logged.

    If called multiple times, then writes this metric as a sequence of values.
    """

    if not isinstance(metric_name, str):
        raise TypeError("key must be 'str'")

    experiment.add_extra_key('metric:' + metric_name, float(value), overwrite=False)


def add_pytorch_model(model):
    pass # TODO
