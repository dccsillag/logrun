"""
Experiment logging utilities for Machine Learning.
"""

from logrun.internals import experiment, Artifact


__all__ = [
    'PyTorchModel',
    'TensorFlowModel',
    'log_metric',
    'log_pytorch_model',
    'log_tensorflow_model',
]


class PyTorchModel(Artifact):
    """
    Implements how to read and write a PyTorch model.

    Note that the current implementation uses `torch.load` and `torch.save`.
    """

    def __init__(self, model):
        self.model = model

    @staticmethod
    def read(path: str) -> None:
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
    def read(path: str) -> None:
        import tensorflow as tf

        return tf.keras.models.load_model(path)

    def write(self, path: str) -> None:
        self.model.save(path)


def log_metric(value: float, metric_name: str) -> None:
    """
    Add a value `value` of a metric identified by `metric_name` to the extra keys to be logged.

    If called multiple times, then writes this metric as a sequence of values.
    """

    if not isinstance(metric_name, str):
        raise TypeError("key must be 'str'")

    experiment.add_extra_key('metric:' + metric_name, float(value), overwrite=False)


def log_pytorch_model(model, key: str = 'trained_model') -> None:
    """
    Add a trained PyTorch model `model` under key `key` (which defaults to `"trained_model"`) to the
    extra keys to be logged.
    """

    if not isinstance(key, str):
        raise TypeError("key must be 'str'")

    experiment.add_extra_key('model:' + key, PyTorchModel(model), overwrite=True)


def log_tensorflow_model(model, key: str = 'trained_model') -> None:
    """
    Add a trained TensorFlow model `model` under key `key` (which defaults to `"trained_model"`) to
    the extra keys to be logged.
    """

    if not isinstance(key, str):
        raise TypeError("key must be 'str'")

    experiment.add_extra_key('model:' + key, TensorFlowModel(model), overwrite=True)
