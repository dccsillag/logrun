"""
Experiment logging utilities for Machine Learning.
"""

from logrun.internals import experiment, Artifact


__all__ = [
    'PyTorchModel',
    'TensorFlowModel',
    'add_metric',
    'add_pytorch_model',
    'add_tensorflow_model',
]


class PyTorchModel(Artifact):
    """
    Implements how to read and write a PyTorch model.

    Note that the current implementation uses `torch.load` and `torch.save`.
    """

    def __init__(self, model):
        self.model = model

    @staticmethod
    def read(path: str):
        import torch

        return torch.load(path)

    def write(self, path: str) -> None:
        import torch

        torch.save(self.model, path)


class TensorFlowModel(Artifact):
    """
    Implements how to read and write a TensorFlow/Keras model.
    """

    def __init__(self, model):
        self.model = model

    @staticmethod
    def read(path: str):
        import tensorflow as tf

        return tf.keras.models.load_model(path)

    def write(self, path: str):
        self.model.save(path)


def add_metric(metric_name, value):
    """
    Add a value `value` of a metric identified by `metric_name` to the extra keys to be logged.

    If called multiple times, then writes this metric as a sequence of values.
    """

    if not isinstance(metric_name, str):
        raise TypeError("key must be 'str'")

    experiment.add_extra_key('metric:' + metric_name, float(value), overwrite=False)


def add_pytorch_model(model, key='trained_model'):
    """
    Add a trained PyTorch model `model` under key `key` (which defaults to `"trained_model"`) to the
    extra keys to be logged.
    """

    if not isinstance(key, str):
        raise TypeError("key must be 'str'")

    experiment.add_extra_key('model:' + key, PyTorchModel(model), overwrite=True)


def add_tensorflow_model(model, key='trained_model'):
    """
    Add a trained TensorFlow model `model` under key `key` (which defaults to `"trained_model"`) to
    the extra keys to be logged.
    """

    if not isinstance(key, str):
        raise TypeError("key must be 'str'")

    experiment.add_extra_key('model:' + key, TensorFlowModel(model), overwrite=True)
