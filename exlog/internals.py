"""
Internal mechanisms for experiment logging.
"""

from typing import List, Dict, Any
from abc import ABC, abstractmethod
import sys
import atexit
import warnings
import os
import subprocess
import tempfile
import platform
import inspect
import shutil
import tarfile
import time
import datetime
import uuid
import pickle

import xxhash
import psutil
import dill
import git


start_timestamp = time.time()
start_datetime = datetime.datetime.now()


def get_script_path():
    path = os.path.abspath(sys.argv[0])
    assert os.path.exists(path)
    return path


def ensure_dir_exists(path):
    path = os.path.abspath(os.path.realpath(path))

    if not os.path.exists(path):
        os.makedirs(path)

    return os.path.abspath(path)


def eval_checksum(path, state=None, digest=True):
    path = os.path.abspath(os.path.realpath(path))

    if state is None:
        state = xxhash.xxh3_64()

    if os.path.isfile(path):
        filesize = os.path.getsize(path)
        available_memory = psutil.virtual_memory().available
        if 10*filesize <= available_memory:
            with open(path, 'rb') as file:
                state.update(file.read())
        else:
            chunksize = max(available_memory//10, state.block_size)
            with open(path, 'rb') as file:
                while True:
                    chunk = file.read(chunksize)
                    if not chunk:
                        break
                    state.update(chunk)
    elif os.path.isdir(path):
        for child in os.listdir(path):
            eval_checksum(os.path.join(path, child), state=state, digest=False)

    if digest:
        return state.hexdigest()


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
    input_files: List[str]
    extra_keys: Dict[str, Any]
    multiple: Dict[str, bool]

    def __init__(self):
        self.uuid = str(uuid.uuid4())
        self.rootpath = os.environ.get('EXLOG_ROOT')
        if self.rootpath is None:
            raise OSError("Environment variable 'EXLOG_ROOT' is not defined!")

        self.has_content = False
        self.output_files = []
        self.input_files = []
        self.extra_keys = {}
        self.multiple = {}

        tmpstdout_handle, self.stdout_file = tempfile.mkstemp()  # 'stdout.out'
        tmpstderr_handle, self.stderr_file = tempfile.mkstemp()  # 'stderr.out'
        os.close(tmpstdout_handle)
        os.close(tmpstderr_handle)

        self._setup_stdout_redirection(self.stdout_file, self.stderr_file)

    def add_output_file(self, path):
        self.has_content = True
        self.output_files.append(path)

    def add_input_file(self, path):
        self.has_content = True
        self.input_files.append(path)

    def add_extra_key(self, key, value, overwrite=True):
        self.has_content = True
        if key in self.extra_keys:
            if overwrite:
                warnings.warn("Overwriting key '%s' in experiment" % key)
                self.extra_keys[key] = value
                self.multiple[key] = False
            else:
                if self.multiple[key]:
                    self.extra_keys[key].append(value)
                else:
                    self.multiple[key] = True
                    self.extra_keys[key] = [self.extra_keys[key], value]
        else:
            self.extra_keys[key] = value
            self.multiple[key] = False

    def _setup_stdout_redirection(self, stdout_file, stderr_file):
        tee_stdout = subprocess.Popen(['tee', stdout_file], stdin=subprocess.PIPE)
        os.dup2(tee_stdout.stdin.fileno(), sys.stdout.fileno())
        tee_stderr = subprocess.Popen(['tee', stderr_file], stdin=subprocess.PIPE)
        os.dup2(tee_stderr.stdin.fileno(), sys.stderr.fileno())

    def _cleanup(self):
        if os.path.exists(self.stdout_file): os.remove(self.stdout_file)
        if os.path.exists(self.stderr_file): os.remove(self.stderr_file)

    def save_experiment(self):
        if not self.has_content:
            self._cleanup()
            return

        print("[Saving experiment: %s]" % self.uuid)

        experiment_path = \
            ensure_dir_exists(os.path.join(self.rootpath, 'all_experiments', self.uuid))
        experiment_path_targz = experiment_path + '.tar.gz'
        experiment_by_outfile_path = \
            ensure_dir_exists(os.path.join(self.rootpath, 'experiments_by_output_file'))
        experiment_by_infile_path = \
            ensure_dir_exists(os.path.join(self.rootpath, 'experiments_by_input_file'))
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
        source_file = sys.argv[0]
        if os.path.getmtime(source_file) > start_timestamp:
            print("Warning: script file [%s] modified since start of execution!")
        with open(os.path.join(experiment_source_directory,
                               os.path.relpath(source_file).replace(os.sep, '%')), 'w') as file:
            with open(source_file) as scriptfile:
                file.write(scriptfile.read())

        with open(os.path.join(experiment_path, 'meta.pickle'), 'wb') as file:
            metadata = {
                'host':                 platform.node(),
                'user':                 os.getlogin(),
                'cwd':                  os.getcwd(),
                'argv':                 sys.argv,
                'start_execution_time': start_datetime,
                'end_execution_time':   datetime.datetime.now(),
                'environment':          dict(os.environ),
            }
            try:
                gitrepo = git.Repo(search_parent_directories=True)
                metadata['gitcommit'] = gitrepo.head.object.hexsha
            except git.exc.InvalidGitRepositoryError:
                pass
            pickle.dump(metadata, file)

        shutil.copyfile(self.stdout_file, os.path.join(experiment_path, 'stdout.out'))
        shutil.copyfile(self.stderr_file, os.path.join(experiment_path, 'stderr.out'))

        output_files_path = ensure_dir_exists(os.path.join(experiment_path, 'output_files'))
        for output_file in self.output_files:
            if not os.path.exists(output_file):
                print("Warning: output file does not exist: '%s'; skipping this one..."
                      % output_file)
                continue

            output_file_repr = output_file.replace(os.sep, '%')
            shutil.copyfile(output_file, os.path.join(output_files_path, output_file_repr))
            os.symlink(experiment_path_targz,
                       os.path.join(ensure_dir_exists(os.path.join(experiment_by_outfile_path,
                                                                   output_file_repr)),
                                    start_datetime.strftime('%Y-%m-%d-%H-%M-%S') + '.' + self.uuid))
        with open(os.path.join(experiment_path, 'input_files.pickle'), 'wb') as file:
            pickle.dump({input_file: eval_checksum(input_file)
                         for input_file in self.input_files},
                        file)

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

        with tarfile.open(experiment_path_targz, 'w:gz') as tar_handle:
            for root, _, files in os.walk(experiment_path):
                for file in files:
                    tar_handle.add(os.path.join(root, file))
        shutil.rmtree(experiment_path)

        self._cleanup()


experiment = Experiment()
atexit.register(experiment.save_experiment)
