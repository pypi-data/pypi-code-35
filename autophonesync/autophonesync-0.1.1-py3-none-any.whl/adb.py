import subprocess
from functools import partial


class AdbWrapper:
    _env = None

    def _run_cmd(self, subcmd, *args, no_empty=False, **options):
        cmd = ['adb', subcmd] + list(args)
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            universal_newlines=True,
            env=self._env,
            **options,
        )
        try:
            for line in proc.stdout:
                if not line:
                    # Should be last line
                    continue
                line = line.rstrip('\n')
                if no_empty and not line:
                    continue
                yield line
            proc.wait()
            if proc.returncode != 0:
                raise subprocess.CalledProcessError(proc.returncode, cmd)
        except GeneratorExit:
            proc.terminate()

    def __getitem__(self, name):
        return partial(self._run_cmd, name)

    def device(self, serialnum):
        aw = AdbWrapper()
        aw._env = {
            'ANDROID_SERIAL': serialnum,
        }

        return aw
