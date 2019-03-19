import os


def credential(instance):
    alias = "AZURE_" + instance
    if os.environ.get(alias + "_DRIVER_PATH"):
        driver = os.environ.get(alias + "_DRIVER_PATH")
    else:
        driver = os.environ.get(alias + "_DRIVER")
    connection_kwargs = {
        'database': os.environ[alias + "_DATABASE"],
        'uid': os.environ[alias + "_USERNAME"],
        'server': os.environ[alias + "_HOST"],
        'port': os.environ[alias + "_PORT"],
        'password': os.environ[alias + "_PASSWORD"],
        'driver': driver,
        'TDS_Version': '7.2'
    }
    return connection_kwargs
