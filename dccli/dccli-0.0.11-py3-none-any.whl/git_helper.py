import os
import subprocess
import traceback
from os.path import join, isdir, exists, normpath
from subprocess import Popen

from clint.textui import prompt, validators

from dccli.constants import *
from dccli.utils import console_out_warn, console_out_log


def pack_code_using_git(out_folder, working_directory):
    # upload current git directory and its sub directories
    repo_tar_path = join(out_folder, CODE_TAR_GZ)

    try:
        # prompt for untracked files
        check_untracked_process = Popen(['git', 'ls-files', '--others', '--exclude-standard'], stdout=subprocess.PIPE, 
            cwd=working_directory)
        check_untracked_process.wait()
        untracked = check_untracked_process.stdout.read().decode("utf-8").split("\n")
            
        if len(untracked) > 1:
            console_out_warn("Skip untracked files in the repo")

        # start packaging code into tar.gz
        # check if there is uncommitted change in the working dir
        diff_process = Popen(
            ['git', 'status', '--porcelain'], stdout=subprocess.PIPE)
        diff_process.wait()
        diffs = diff_process.stdout.read().decode("utf-8").split("\n")

        # if there is no diff, process will output empty string
        if len(diffs) - len(untracked) > 1:
            # user has uncommitted change in working directory
            console_out_warn("Code package includes uncommitted changes")

            stash_process = Popen(['git', 'stash'], stdout=subprocess.PIPE)
            stash_process.wait()

            archive_process = Popen(
                ['git', 'archive', '--format={}'.format(TAR_GZ_EXTENSION), 'stash@{0}',
                    '--output={}'.format(repo_tar_path)],
                    stderr=subprocess.PIPE,
                    cwd=working_directory)

            console_out_log("zip source code...")
            archive_process.wait()
            pop_stash_process = Popen(
                ['git', 'stash', 'pop'], stdout=subprocess.PIPE)
            pop_stash_process.wait()
        else:
            archive_process = Popen(['git', 'archive', '--format={}'.format(
                TAR_GZ_EXTENSION), 'HEAD', '--output={}'.format(repo_tar_path)],
                stderr=subprocess.PIPE,
                cwd=working_directory)

            console_out_log("zip source code...")
            archive_process.wait()

        if not exists(repo_tar_path):
            return False, "Failed to pack the code"
        else:
            return True, repo_tar_path

    except:
        if DEBUG:
            traceback.print_exc()

        return False, "Failed to pack the code"

def get_repo_toplevel_dir():
    process = Popen(
        ['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE)
    process.wait()
    toplevel = process.stdout.read().decode("utf-8").strip('\n')
    if not isdir(toplevel):
        return None
    return normpath(toplevel)
