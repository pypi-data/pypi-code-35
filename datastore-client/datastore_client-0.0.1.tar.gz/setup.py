# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['datastore_client']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-datastore>=1.7,<2.0']

setup_kwargs = {
    'name': 'datastore-client',
    'version': '0.0.1',
    'description': 'A simple Google DataStore client',
    'long_description': "# Simple DataStore Client\n\nA simple Google DataStore client that exposes 3 functions.\n\n```python\ndef set_key(entity_name: str, key_name: str, **properties: Any) -> None:\n    ...\n```\n\n```python\ndef get_key(entity_name: str, key_name: str) -> Optional[Entity]:\n    ...\n```\n\n```python\ndef query_entity(\n    entity_name: str,\n    *query_filters: Tuple[str, str, Any],\n    projection: List[str]=None,\n    limit: Optional[int]=None,\n) -> Iterator:\n    ...\n```\n\n## Examples\n\n### `set_key`\n\n```python\nset_key(\n    entity_name=RECHARGE_NOTES_ENTITY, \n    key_name=note_key, \n    username=username, \n    reference=reference, \n    note=notes,\n)\n```\n\n### `get_key`\n\n```python\nget_key(LOGIN_ENTITY, username)\n```\n\n### `query_entity`\n\n```python\nproduct_list = list(query_entity(\n    PRODUCT_ENTITY,\n    ('network', '=', network_name),\n    ('product_type', '=', product_code),\n    ('bundle_size', '=', denomination),\n    projection=['id'],\n    limit=1,\n))\n\nprint(product_list[0]['id'])\n```\n",
    'author': 'Jethro Muller',
    'author_email': 'git@jethromuller.co.za',
    'url': 'https://github.com/Flickswitch/datastore-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
