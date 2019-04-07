# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pypika_gis']

package_data = \
{'': ['*']}

install_requires = \
['PyPika>=0.26.0,<0.27.0']

setup_kwargs = {
    'name': 'pypika-gis',
    'version': '1.2.0',
    'description': 'SpatialTypes functions for extend PyPika with GIS',
    'long_description': '# pypika-gis\n\nSpatialTypes functions for extend [PyPika](https://github.com/kayak/pypika) with GIS.\n\n## Example\n\n```python\nfrom pypika import Query\nfrom pypika_gis import spatialtypes as st\n\nquery = Query.from_(\'field\').select(\'id\', st.AsGeoJSON(\'geom\'))\nprint(str(query))\n# SELECT "id",ST_AsGeoJSON(\'geom\') FROM "field"\n\nquery = Query.from_(\'crop\').select(\'id\').where(st.Intersects(\'geom\', st.SRID(st.MakePoint(10, 5), 4326)))\nprint(str(query))\n# SELECT "id" FROM "crop" WHERE ST_Intersects(\'geom\',ST_SRID(ST_MakePoint(10,5),4326))\n```\n\n## Available functions\n\n- Envelope(ST_Envelope)\n- Extent(ST_Extent)\n- GeomFromGeoJSON(ST_GeomFromGeoJSON)\n- GeoHash(ST_GeoHash)\n- Intersection(ST_Intersection)\n- Intersects(ST_Intersects)\n- IsEmpty(ST_IsEmpty)\n- IsValid(ST_IsValid)\n- MakePoint(ST_MakePoint)\n- SetSRID(ST_SetSRID)\n- Within(ST_Within)\n- X(ST_X)\n- Y(ST_Y)\n- Z(ST_Z)\n\n## Dependencies\n\n- [PyPika](https://github.com/kayak/pypika)\n\n## Setup\n\n```bash\npip install pypika-gis\n```\n\n## Development\n\nFull tests and coverage\n\n```bash\npip install -r requirements-dev.txt\npython -m pytest --cov\n```\n\n## Credits\n\npypika-gis is based on [PyPika](https://github.com/kayak/pypika). Check their page for further query buider instructions, examples and more details about PyPika core.\n',
    'author': 'Eduardo G. S. Pereira',
    'author_email': 'edu_vcd@hotmail.com',
    'url': 'https://github.com/eduardogspereira/pypika-gis',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
