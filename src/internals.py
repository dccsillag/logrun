"""
Internal mechanisms for experiment logging.
"""

from typing import List, Dict, Any
from abc import ABC, abstractmethod
import sys
import atexit
import os
import platform
import inspect
import shutil
import tarfile
import time
import datetime
import uuid
import pickle

import dill


start_timestamp = time.time()
start_datetime = datetime.datetime.now()


def get_script_path():
    path = os.path.abspath(sys.argv[0])
    assert os.path.exists(path)
    return path


def ensure_dir_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

    return os.path.abspath(path)


class Artifact(ABC):
    @abstractmethod
    def write(self, path: str):
        pass

    @abstractmethod
    def read(self, path: str):
        pass


# pylint: disable=too-few-public-methods
class Experiment:
    uuid: str
    rootpath: str

    has_content: bool
    output_files: List[str]
    extra_keys: Dict[str, Any]

    def __init__(self):
        self.uuid = str(uuid.uuid4())
        self.rootpath = os.environ.get('MICROLOG_ROOT')
        if self.rootpath is None:
            raise OSError("Environment variable 'MICROLOG_ROOT' is not defined!")

        self.has_content = False
        self.output_files = []
        self.extra_keys = {}

    def add_output_file(self, path):
        self.has_content = True
        self.output_files.append(path)

    def add_extra_key(self, key, value):
        self.has_content = True
        self.extra_keys[key] = value

    def save_experiment(self):
        if not self.has_content:
            return

        print("[Saving experiment: %s]" % self.uuid)

        experiment_path = \
            ensure_dir_exists(os.path.join(self.rootpath, 'all_experiments', self.uuid))
        experiment_by_file_path = \
            ensure_dir_exists(os.path.join(self.rootpath, 'experiments_by_path'))
        experiment_source_directory = ensure_dir_exists(os.path.join(experiment_path, 'source'))

        for module in sys.modules.values():
            if not module.__name__.startswith('src.'):
                continue

            source_file = inspect.getsourcefile(module)

            if os.path.getmtime(source_file) > start_timestamp:
                print("Warning: source file [%s] modified since start of program execution!")

            with open(os.path.join(experiment_source_directory,
                                   os.path.relpath(source_file).replace(os.sep, '%')), 'w') \
                    as file:
                file.write(inspect.getsource(module))

        with open(os.path.join(experiment_path, 'meta.pickle'), 'wb') as file:
            pickle.dump({
                'host':                 platform.node(),
                'user':                 os.getlogin(),
                'cwd':                  os.getcwd(),
                'argv':                 sys.argv,
                'start_execution_time': start_datetime,
                'end_execution_time':   datetime.datetime.now(),
            }, file)

        output_files_path = ensure_dir_exists(os.path.join(experiment_path, 'output_files'))
        for output_file in self.output_files:
            if not os.path.exists(output_file):
                print("Warning: output file does not exist: '%s'; skipping this one..."
                      % output_file)
                continue

            output_file_repr = output_file.replace(os.sep, '%')
            shutil.copyfile(output_file, os.path.join(output_files_path, output_file_repr))
            os.symlink(experiment_path,
                       os.path.join(ensure_dir_exists(os.path.join(experiment_by_file_path,
                                                                   output_file_repr)),
                                    start_datetime.strftime('%Y-%m-%d-%H-%M-%S') + '.' + self.uuid))

        extra_keys_path = ensure_dir_exists(os.path.join(experiment_path, 'extra_keys'))

        for key, value in self.extra_keys.items():
            path = os.path.join(extra_keys_path, key)
            if isinstance(value, Artifact):
                value.write(path)
                with open(path + '.read', 'wb') as file:
                    dill.dump(value.read, file)
            else:
                with open(path, 'wb') as file:
                    dill.dump(value, file)


experiment = Experiment()
atexit.register(experiment.save_experiment)
