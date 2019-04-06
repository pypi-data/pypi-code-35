from getpass import getpass

try:
    import keyring
    access_token = keyring.get_password("system", "grepme")
    if access_token is None:
        access_token = getpass("Groupme Access token: ")
        keyring.set_password("system", "grepme", access_token)
except ImportError:
    try:
        import warning
    except ImportError:
        import warnings as warning
    warning.warn("keyring not installed: passwords are exposed on the filesystem")
