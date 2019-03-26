from django.core.management import ManagementUtility
import click
import os


@click.command()
@click.argument('project_name', type=str)
def start(project_name):
    try:
        __import__(project_name)
    except ImportError:
        pass
    else:
        click.echo(
            '\'%s\' conflicts with the name of an existing '
            'Python module and cannot be used as a project '
            'name. Please try another name.' % project_name
        )

        raise SystemExit(1)

    click.echo()
    click.echo('Creating a Delbot project called %s.' % project_name)

    template_path = os.path.join(
        os.path.dirname(
            os.path.dirname(__file__)
        ),
        'project_template'
    )

    utility = ManagementUtility(
        [
            'django-admin.py',
            'startproject',
            '--template=%s' % template_path,
            '--extension=py,env,editorconfig',
            project_name
        ]
    )

    utility.execute()

    project_path = os.path.join(
        os.getcwd(),
        project_name
    )

    open(
        os.path.join(
            project_path,
            '.gitignore'
        ),
        'w'
    ).write(
        '__pycache__\n',
        '.coverage\n'
        '.env\n'
        '*.egg-info\n'
        '*.pyc\n'
        '/bin\n'
        '/include\n'
        '/lib\n'
        '/man\n'
        '/pip-selfcheck.json\n'
        '/pyvenv.cfg\n'
        'db.sqlite3\n'
        'htmlcov\n'
    )

    click.echo()
    click.echo(
        (
            'Well, that all looks to be in order. In the newly-created '
            '%(project_name)s directory, you\'ll find a Django project already '
            'configured. Feel free to adapt it to your needs. \n\n'
            'You\'ll also find an environment file, with a secret key for '
            'local development. You can use a package like python-dotenv '
            '(https://github.com/theskumar/python-dotenv) to activate the .env '
            'file. Once you\'re ready to go, run the following:\n\n'
            '    cd %(project_name)s\n'
            '    pip install -r requirements-testing.txt\n'
            '    pip install -r requirements.txt\n'
            '    python manage.py migrate\n'
            '    python manage.py runserver\n\n'
            'Good luck!\n'
        ) % {
            'project_name': project_name
        }
    )


@click.group()
def main():
    """A service status blog for SaaS applications"""


main.add_command(start)
