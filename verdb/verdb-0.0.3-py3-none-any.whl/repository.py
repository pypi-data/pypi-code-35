import platform
from contextlib import contextmanager
from pathlib import Path
from subprocess import run, CalledProcessError
from tempfile import TemporaryDirectory


class Repository:
    repositories = {}

    def __new__(cls, prefix):
        prefix = Path(prefix).resolve()
        if prefix in cls.repositories:
            return cls.repositories[prefix]
        else:
            return super().__new__(cls)

    def __init__(self, prefix):
        self.prefix = prefix
        self._work_tree = None
        self._index = None

    def git(self, *args, **kwargs):
        command = ['git'] + [str(arg) for arg in args if arg]
        env = {
            **{f'GIT_{key.upper()}': str(value) for key, value in kwargs.items() if value},
            **{'GIT_DIR': str(Path(self.prefix, '.git').resolve())},
            **({'GIT_INDEX_FILE': str(self._index)} if self._index else {}),
            **({'GIT_WORK_TREE': str(self._work_tree)} if self._work_tree else {})
        }
        cwd = str(self._work_tree) if self._work_tree else str(Path(self.prefix).resolve())
        result = run(command, cwd=cwd, env=env, capture_output=True)

        try:
            result.check_returncode()
            return result.stdout.decode('utf-8').strip()
        except CalledProcessError:
            raise ValueError(result.stderr.decode('utf-8').strip())

    @contextmanager
    def commit(self, message):
        if self._index or self._work_tree:
            yield self._work_tree
            return

        with TemporaryDirectory() as self._index, TemporaryDirectory() as self._work_tree:
            self._index = str(Path(self._index, 'index').resolve())
            self.git('reset', index_file=self._index)

            yield self._work_tree

            self.git(
                'commit',
                '--allow-empty',
                '--allow-empty-message',
                f'--message={message}',
                index_file=self._index,
                author_name='VerDB',
                author_email=f'verdb@{platform.node()}',
                committer_name='VerDB',
                committer_email=f'verdb@{platform.node()}')
            self._index = self._work_tree = None
