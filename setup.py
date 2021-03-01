from setuptools import setup
import os

# this won't be used, but is needed in order to import logrun successfully:
os.environ['LOGRUN_ROOT'] = 'logrun-root-tmp'

from logrun import __version__


this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md')) as file:
    long_description = file.read()



setup(
    name="logrun",
    version=__version__,
    description="A convenient experiment logging package for Python",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/dccsillag/logrun",
    author="Daniel Csillag",
    author_email="dccsillag@gmail.com",
    license="MIT",
    packages=['logrun', 'logrun.utils'],
    install_requires=['dill',
                      'psutil',
                      'xxhash',
                      'gitpython'],
    extras_require={
        'utils-media': ['numpy', 'imageio'],
        'utils-data': ['numpy', 'pandas'],
        'utils-ml-cpu': ['tensorflow',     'torch==+cpu'],
        'utils-ml-gpu': ['tensorflow-gpu', 'torch'],
    }

    # TODO: classifiers
)
