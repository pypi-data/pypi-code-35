from guillotina import configure

app_settings = {
    'store_json': True,
    "load_utilities": {
        "catalog": {
            "provides": "guillotina.interfaces.ICatalogUtility",
            "factory": "guillotina_pgcatalog.utility.PGSearchUtility",
            "settings": {}
        }
    },
}


def includeme(root):
    configure.scan('guillotina_pgcatalog.api')
