import os
from invoke import task, run
from gitannexgui.gitannex import GitAnnex


@task
def clean(ctxt):
    run("rm dist/*")


@task
def build(ctxt):
    # build resources
    #run('rcc -binary qml.qrc -o qml.rcc')
    run('python setup.py sdist bdist_wheel')


@task
def publish(ctxt):
    run('git push gitlab')
    run('twine upload dist/*')
