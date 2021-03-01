"""
Experiment logging utilities for media (images, videos, etc.).
"""

import numpy as np
import imageio

from logrun.internals import experiment, Artifact


__all__ = [
    'ImageArtifact',
    'VideoArtifact',
    'add_image',
    'add_video',
]


class ImageArtifact(Artifact):
    """
    Implements how to read and write an image.
    """

    def __init__(self, data):
        self.data = np.asarray(data)

    @staticmethod
    def read(path):
        return imageio.imread(path, format='png')

    def write(self, path):
        imageio.imwrite(path, self.data, format='png')


class VideoArtifact(Artifact):
    """
    Implements how to read and write a video.
    """

    def __init__(self, frames):
        if isinstance(frames, np.ndarray) and frames.ndim == 3:
            self.frames = frames
        else:
            self.frames = np.array([np.asarray(frame) for frame in frames])

    @staticmethod
    def read(path):
        return np.array(imageio.mimread(frames, format='mp4'))

    def write(self, path):
        imageio.mimwrite(path, self.frames, format='mp4', output_params=['-f', 'mp4'])


def add_image(key, image, overwrite=False):
    """
    Add an image identified by `key` to the extra keys to be logged.

    If called multiple times with `overwrite` set to `False`, then writes this key as a sequence of
    images.
    """

    if not isinstance(key, str):
        raise TypeError("key must be 'str'")

    experiment.add_extra_key(key, ImageArtifact(image), overwrite=overwrite)


def add_video(key, frames, overwrite=False):
    """
    Add a video (sequence of frames) identified by `key` to the extra keys to be logged.

    If called multiple times with `overwrite` set to `False`, then writes this key as a sequence of
    videos.
    """

    if not isinstance(key, str):
        raise TypeError("key must be 'str'")

    experiment.add_extra_key(key, VideoArtifact(frames), overwrite=overwrite)
