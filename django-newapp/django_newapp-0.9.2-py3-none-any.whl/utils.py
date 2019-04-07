import os

def get_app_template_dir():
    return os.path.dirname(__file__) + "/app_templates"

def get_app_template_path(name):
    return os.path.dirname(__file__) + "/app_templates/" + name

def get_app_templates():
    data = []

    for template in os.listdir(get_app_template_dir()):
        desc_file = os.path.join(get_app_template_dir(), "%s/desc.txt" % template)
        with open(desc_file, 'r') as desc:
            data.append({
                'name': template,
                'desc': desc.read()
            })
    return data