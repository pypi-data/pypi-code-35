from graphenestorage import (
    InRamConfigurationStore,
    InRamPlainKeyStore,
    InRamEncryptedKeyStore,
    SqliteConfigurationStore,
    SqlitePlainKeyStore,
    SqliteEncryptedKeyStore,
    SQLiteFile
)

url = "ws://mainnet-api.quantachain.io"
InRamConfigurationStore.setdefault("node", url)
SqliteConfigurationStore.setdefault("node", url)


def get_default_config_store(*args, **kwargs):
    if "appname" not in kwargs:
        kwargs["appname"] = "quantadex"
    return SqliteConfigurationStore(*args, **kwargs)


def get_default_key_store(config, *args, **kwargs):
    if "appname" not in kwargs:
        kwargs["appname"] = "quantadex"
    return SqliteEncryptedKeyStore(
        config=config, **kwargs
    )
