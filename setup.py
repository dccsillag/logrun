from setuptools import setup
import os


this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md')) as file:
    long_description = file.read()



setup(
    name="logrun",
    version="0.1.0",
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
