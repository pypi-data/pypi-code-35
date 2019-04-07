def echo(command):
    execute(f"echo {command}")


def execute(command, cwd=None, env=None, shell=True):
    try:
        from collections import namedtuple
        import subprocess
        print(command)
        proc = subprocess.run(
            command,
            cwd=cwd,
            check=True,
            encoding="utf-8",
            env=env,
            shell=shell,
            stdout=subprocess.PIPE,
        )
        print(proc.stdout)
        if proc.returncode != 0:
            print(proc.stderr)
        output = namedtuple("output", ["stdout", "stderr", "returncode"])
        return output(proc.stdout, proc.stderr, proc.returncode)
    except subprocess.CalledProcessError as e:
        print(e.output)
        raise


def remove_files(directory, cwd):
    return execute(f"rm -rf {directory}", cwd)


def zip(output_filename, dir_name, format="zip"):
    import shutil

    shutil.make_archive(output_filename, format, dir_name)


def unzip(path_to_zip_file, directory_to_extract_to):
    import zipfile

    zip_ref = zipfile.ZipFile(path_to_zip_file, "r")
    zip_ref.extractall(directory_to_extract_to)
    zip_ref.close()
