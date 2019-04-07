from invoke import task


def mine(ctx):
    pass


@task(mine)
def mytask(ctx):
    pass
