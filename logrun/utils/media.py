"""
Experiment logging utilities for media (images, videos, etc.).
"""

from typing import Union, Iterable

from logrun.internals import experiment, Artifact


__all__ = [
    'ImageArtifact',
    'VideoArtifact',
    'log_image',
    'log_video',
]


class ImageArtifact(Artifact):
    """
    Implements how to read and write an image.
    """

    def __init__(self, data: 'np.ndarray'):
        import numpy as np

        self.data = np.asarray(data)

    @staticmethod
    def read(path: str) -> None:
        from imageio import imread

        return imread(path, format='png')

    def write(self, path: str) -> None:
        from imageio import imwrite

        imwrite(path, self.data, format='png')


class VideoArtifact(Artifact):
    """
    Implements how to read and write a video.
    """

    def __init__(self, frames: Union[Iterable['np.ndarray'], 'np.ndarray']):
        import numpy as np

        if isinstance(frames, np.ndarray) and frames.ndim == 3:
            self.frames = frames
        else:
            self.frames = np.array([np.asarray(frame) for frame in frames])

    @staticmethod
    def read(path: str) -> None:
        import numpy as np
        from imageio import mimread

        return np.array(mimread(path, format='mp4'))

    def write(self, path: str) -> None:
        from imageio import mimwrite

        mimwrite(path, self.frames, format='mp4', output_params=['-f', 'mp4'])


def log_image(image: 'np.ndarray', key: str, overwrite: bool = False) -> None:
    """
    Add an image identified by `key` to the extra keys to be logged.

    If called multiple times with `overwrite` set to `False`, then writes this key as a sequence of
    images.
    """

    if not isinstance(key, str):
        raise TypeError("key must be 'str'")

    experiment.add_extra_key(key, ImageArtifact(image), overwrite=overwrite)


def log_video(frames: Union[Iterable['np.ndarray'], 'np.ndarray'], key: str, overwrite: bool = False) \
        -> None:
    """
    Add a video (sequence of frames) identified by `key` to the extra keys to be logged.

    If called multiple times with `overwrite` set to `False`, then writes this key as a sequence of
    videos.
    """

    if not isinstance(key, str):
        raise TypeError("key must be 'str'")

    experiment.add_extra_key(key, VideoArtifact(frames), overwrite=overwrite)
