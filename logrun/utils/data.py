"""
Experiment logging utilities for data.
"""

from typing import Union

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

    def __init__(self, data: 'np.ndarray'):
        import numpy as np

        self.data = np.asarray(data)

    @staticmethod
    def read(path: str) -> None:
        import numpy as np

        return np.load(path)

    def write(self, path: str) -> None:
        import numpy as np

        with open(path, 'wb') as file:
            np.save(file, self.data)


class PandasArtifact(Artifact):
    """
    Implements how to read and write a Pandas Series or DataFrame.
    """

    def __init__(self, data: Union['pd.Series', 'pd.DataFrame']):
        import pandas as pd

        assert isinstance(data, (pd.Series, pd.DataFrame))

        self.data = data

    @staticmethod
    def read(path: str) -> Union['pd.Series', 'pd.DataFrame']:
        import pandas as pd

        return pd.read_hdf(path)

    def write(self, path: str) -> None:
        self.data.to_hdf(path, 'data')


def log_ndarray(array, key: str, overwrite: bool = False) -> None:
    """
    Add a NumPy arrray identified by `key` to the extra keys to be logged.

    If called multiple times with `overwrite` set to `False`, then writes this key as a sequence of
    arrays.
    """

    if not isinstance(key, str):
        raise TypeError("key must be 'str'")

    experiment.add_extra_key(key, NumpyArtifact(array), overwrite=overwrite)


def log_series(series: 'pd.Series', key: str, overwrite: bool = False) -> None:
    """
    Add a Pandas Series identified by `key` to the extra keys to be logged.

    If called multiple times with `overwrite` set to `False`, then writes this key as a sequence of
    series.
    """

    import pandas as pd

    if not isinstance(key, str):
        raise TypeError("key must be 'str'")
    if not isinstance(series, pd.Series):
        raise TypeError("series must be a Pandas Series")

    experiment.add_extra_key(key, PandasArtifact(series), overwrite=overwrite)


def log_dataframe(dataframe: 'pd.DataFrame', key: str, overwrite: bool = False) -> None:
    """
    Add a Pandas DataFrame identified by `key` to the extra keys to be logged.

    If called multiple times with `overwrite` set to `False`, then writes this key as a sequence of
    dataframes.
    """

    import pandas as pd

    if not isinstance(key, str):
        raise TypeError("key must be 'str'")
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("dataframe must be a Pandas DataFrame")

    experiment.add_extra_key(key, PandasArtifact(dataframe), overwrite=overwrite)
