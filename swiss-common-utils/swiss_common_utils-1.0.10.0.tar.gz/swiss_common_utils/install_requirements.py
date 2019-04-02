import os


def get_current_folder():
    return os.path.dirname(os.path.realpath(__file__))


def get_required_packages():
    curr_folder = get_current_folder()
    requirements_txt = os.path.join(curr_folder, 'requirements.txt')
    f = open(requirements_txt, 'r')
    install_requires = []
    for pkg in f.readlines():
        install_requires.append(pkg.strip())

    return install_requires

