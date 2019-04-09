import unittest
from pyquilted.builder.projects import ProjectsBuilder
from pyquilted.yaml_loader import YamlLoader


class TestBuilderProjects(unittest.TestCase):
    def test_mapper_projects(self):
        with open('test/validations/projects.yml') as f:
            data = YamlLoader.ordered_load(f)
        mapper = ProjectsBuilder(data['projects'])
        projects = mapper.deserialize()

        valid = {
                'projects': {
                    'label': 'Projects',
                    'icon': 'fa-code',
                    'blocks': [{
                        'name': 'Wight Hunt',
                        'description': 'Lead a small team north to '
                                'capture a wight alive',
                        'icon': 'fa-film',
                        'link': None,
                        'slugs': ['Mission complete', 'Saved by my uncle']
                    }]
                }}
        self.assertEqual(projects.serialize(), valid)


if __name__ == '__main__':
    unittest.main()
