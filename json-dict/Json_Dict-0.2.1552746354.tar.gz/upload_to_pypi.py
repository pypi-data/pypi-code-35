import os
import subprocess
import sys
import time


def create_n_upload():
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    some_command = sys.executable + " " + os.path.basename(__file__) + " sdist bdist_wheel"
    p = subprocess.Popen(some_command, stdout=subprocess.PIPE)
    while True:
        output = p.stdout.readline().decode("utf-8")
        if output == '' and p.poll() is not None:
            break
        if output:
            print(output.strip())
        time.sleep(0.1)
    rc = p.poll()
    return
    some_command = sys.executable + " -m twine upload dist/*"
    p = subprocess.Popen(so,me_command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    print("Command output: ", output.decode("utf-8"))

if __name__ is "__main__":
    if len(sys.argv) == 1:
        create_n_upload()
else:
    import setuptools
    from setup import setup
    setup = setup
    setup['version']=setup['version']+"."+str(int(time.time()))
    print(setup['version'])
    setuptools.setup(
        **setup
    )