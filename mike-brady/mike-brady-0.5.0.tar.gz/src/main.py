import click
from git import Repo
import os
import sys
import glob
import shutil
import json
from jinja2 import Environment, FileSystemLoader


repo = None


def clone_repo(source_repo, target_path, force):
    if (os.path.exists(target_path)):
        if not force:
            print('ERROR: Target folder exists . . . use --force-delete if you want to delete.')
            sys.exit()
        shutil.rmtree(target_path)
    Repo.clone_from(source_repo, target_path)


def remove_git_stuff(target_path):
    basedir = os.path.abspath(target_path)
    for dirpath, dirnames, filenames in os.walk(basedir):
        for d in dirnames:
            if d == '.git':
                shutil.rmtree(os.path.join(dirpath, d))
            lst = glob.glob(os.path.join(dirpath, d, '.gitignore'))
            for fname in lst:
                os.remove(os.path.join(dirpath, d, fname))


def render_templates(target_path, replace_values, file_types):
    basedir = os.path.abspath(target_path)
    for root, dirnames, files in os.walk(basedir):
        for d in dirnames:
            rendered_d = Environment().from_string(d).render(replace_values)
            if not d == rendered_d:
                print('Renaming {} to {}'.format(d, rendered_d))
                os.rename(os.path.join(root, d), os.path.join(root, rendered_d))
        for f in files:
            skip = True
            full_path = os.path.join(root, f)
            for ft in file_types:
                if f.endswith('.{}'.format(ft)):
                    skip = False
                    continue
            if skip:
                continue
            env = Environment(loader=FileSystemLoader(root))
            template = env.get_template(f)
            rendered = template.render(replace_values)
            with open(full_path, "w") as fh:
                print('Writing {}'.format(full_path))
                fh.write(rendered)


@click.command()
@click.argument('source_repo', required=True)
@click.argument('target_path', required=True)
@click.argument('replace_values', required=True)
@click.argument('file_types', required=True)
@click.option('--force-delete/--do_not_force_delete', default=False)
def main(source_repo, target_path, replace_values, file_types, force_delete):
    clone_repo(source_repo, target_path, force_delete)
    remove_git_stuff(target_path)
    render_templates(target_path, json.loads(replace_values), file_types.split(','))


if __name__ == '__main__':
    main()
