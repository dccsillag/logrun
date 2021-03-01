"""
Experiment logging utilities for data.
"""

import numpy as np
import pandas as pd

from logrun.internals import experiment, Artifact


__all__ = [
    'NumpyArtifact',
    'PandasArtifact',
    'log_ndarray',
    'log_series',
    'log_dataframe',
]


class NumpyArtifact(Artifact):
    """
    Implements how to read and write a raw NumPy array.
    """

    def __init__(self, data):
        self.data = np.asarray(data)

    @staticmethod
    def read(path):
        return np.load(path)

    def write(self, path):
        with open(path, 'wb') as file:
            np.save(file, self.data)


class PandasArtifact(Artifact):
    """
    Implements how to read and write a Pandas Series or DataFrame.
    """

    def __init__(self, data):
        assert isinstance(data, (pd.Series, pd.DataFrame))

        self.data = data

    @staticmethod
    def read(path):
        return pd.read_hdf(path)

    def write(self, path):
        self.data.to_hdf(path, 'data')


def log_ndarray(array, key, overwrite=False):
    """
    Add a NumPy arrray identified by `key` to the extra keys to be logged.

    If called multiple times with `overwrite` set to `False`, then writes this key as a sequence of
    arrays.
    """

    if not isinstance(key, str):
        raise TypeError("key must be 'str'")

    experiment.add_extra_key(key, NumpyArtifact(array), overwrite=overwrite)


def log_series(series, key, overwrite=False):
    """
    Add a Pandas Series identified by `key` to the extra keys to be logged.

    If called multiple times with `overwrite` set to `False`, then writes this key as a sequence of
    series.
    """

    if not isinstance(key, str):
        raise TypeError("key must be 'str'")
    if not isinstance(series, pd.Series):
        raise TypeError("series must be a Pandas Series")

    experiment.add_extra_key(key, PandasArtifact(series), overwrite=overwrite)


def log_dataframe(dataframe, key, overwrite=False):
    """
    Add a Pandas DataFrame identified by `key` to the extra keys to be logged.

    If called multiple times with `overwrite` set to `False`, then writes this key as a sequence of
    dataframes.
    """

    if not isinstance(key, str):
        raise TypeError("key must be 'str'")
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("dataframe must be a Pandas DataFrame")

    experiment.add_extra_key(key, PandasArtifact(dataframe), overwrite=overwrite)
