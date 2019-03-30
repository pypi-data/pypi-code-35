# -*- coding: utf-8 -*-
from graphenestorage import (
    InRamConfigurationStore,
    InRamEncryptedKeyStore,
    InRamPlainKeyStore,
    SqliteConfigurationStore,
    SqliteEncryptedKeyStore,
    SQLiteFile,
    SqlitePlainKeyStore,
)


url = "ws://127.0.0.1:7738"
SqliteConfigurationStore.setdefault("node", url)
SqliteConfigurationStore.setdefault("order-expiration", 356 * 24 * 60 * 60)


def get_default_config_store(*args, **kwargs):
    if "appname" not in kwargs:
        kwargs["appname"] = "dexstore"
    return SqliteConfigurationStore(*args, **kwargs)


def get_default_key_store(config, *args, **kwargs):
    if "appname" not in kwargs:
        kwargs["appname"] = "dexstore"
    return SqliteEncryptedKeyStore(config=config, **kwargs)
