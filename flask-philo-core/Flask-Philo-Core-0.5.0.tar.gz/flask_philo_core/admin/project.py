import os
from jinja2 import Template

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


def create_from_template(**data):
    template_folder = os.path.join(BASE_DIR, 'templates', 'project')
    path = data['path']
    filename = data['filename']
    resource_path = os.path.join(template_folder, filename)

    template_parameters = data.get('template_parameters', {})

    with open(resource_path, 'r') as f:
        t = Template(f.read())
        template = t.render(**template_parameters)

    with open(os.path.join(path, filename), 'w') as f:
        f.write(template)
        if template:
            f.write('\n')


def create_docker_files(location, project_extensions):
    compose_params = {}

    for ext in project_extensions:
        compose_params[ext.split('Flask-Philo-')[-1]] = True

    template_location = os.path.join(location, 'tools')

    create_from_template(**{
        'template_parameters': compose_params,
        'path': template_location,
        'filename': 'Dockerfile.python',
    })

    create_from_template(**{
        'template_parameters': compose_params,
        'path': template_location,
        'filename': 'docker-compose.yml',
    })

    create_from_template(**{
        'template_parameters': compose_params,
        'path': template_location,
        'filename': 'Dockerfile.python',
    })

    if 'Flask-Philo-SQLAlchemy' in project_extensions:
        create_from_template(**{
            'template_parameters': compose_params,
            'path': template_location,
            'filename': 'Dockerfile.postgresql',
        })


def create_requirements_file(location, project_extensions):
    params = {}

    for ext in project_extensions:
        params[ext.split('Flask-Philo-')[-1]] = True

    template_location = os.path.join(location, 'tools')

    create_from_template(**{
        'template_parameters': params,
        'path': template_location,
        'filename': 'requirements.txt',
    })


def initialize_src(location, project_extensions, project_name):
    # source code files
    folders = (
        'app', 'config', 'commands', 'tests')

    for folder in folders:
        os.mkdir(os.path.join(location, 'src', folder))
        f = open(
            os.path.join(
                os.path.join(location, 'src', folder), '__init__.py'), 'x')
        f.close()

    def initialize_app():
        template_location = os.path.join(location, 'src', 'app')
        create_from_template(**{
            'path': template_location,
            'filename': 'urls.py',
        })
        create_from_template(**{
            'path': template_location,
            'filename': 'example_views.py',
        })

        template_location = os.path.join(location, 'src', 'config')

        create_from_template(**{
            'path': template_location,
            'filename': 'settings.py',
        })

        template_location = os.path.join(location, 'src', 'tests')
        create_from_template(**{
            'path': template_location,
            'filename': 'test_views.py',
        })

        template_location = os.path.join(location, 'src', 'commands')
        create_from_template(**{
            'path': template_location,
            'filename': '__init__.py',
        })

        template_location = os.path.join(location, 'src', 'commands')
        create_from_template(**{
            'path': template_location,
            'filename': 'hello.py',
        })

        if 'Flask-Philo-SQLAlchemy' in project_extensions:
            template_location = os.path.join(location, 'src', 'app')
            create_from_template(**{
                'path': template_location,
                'filename': 'sqlalchemy_model.py',
                'template_parameters': {
                    'project_name': project_name
                }
            })

    initialize_app()


def start_project():
    project_name = input('Please enter the project name: ')
    location = os.path.join(os.getcwd(), project_name)
    print('Default location for this project is: {}'.format(location))
    cont = ''

    while cont.lower() not in ('yes', 'no',):
        cont = input('\nContinue? YES/NO: ')

    if 'no' == cont:
        exit

    if os.path.exists(location):
        print('ERROR: Location {} already exists'.format(location))
        exit(1)

    os.mkdir(location)

    root_folders = ('documentation', 'src', 'tools')

    for folder in root_folders:
        os.mkdir(os.path.join(location, folder))

    create_from_template(**{
        'template_parameters': {'project_name': project_name},
        'path': location,
        'filename': 'README.md',
    })

    philo_extensions = (
        'Flask-Philo-SQLAlchemy', 'Flask-Philo-Redis',
        'Flask-Philo-Elasticsearch'
    )

    project_extensions = []

    for ext in philo_extensions:
        def ask(ext):
            r = input(
                'Add {} to requirements.txt? YES/NO'
                '(Default NO): '.format(ext))

            if r.lower() not in ('yes', 'no', ''):
                ask(ext)

            elif 'yes' == r.lower():
                project_extensions.append(ext)
        ask(ext)

    # Docker environments
    create_docker_files(location, project_extensions)

    # pip requirements.txt file
    create_requirements_file(location, project_extensions)

    # create src files and directories
    initialize_src(location, project_extensions, project_name)
