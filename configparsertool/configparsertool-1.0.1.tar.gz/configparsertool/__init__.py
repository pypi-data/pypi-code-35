try:
    import ConfigParser as configparser
except Exception:
    import configparser


def getvalues(filepath, section, keys):
    parser = configparser.ConfigParser()
    if not parser.read(filepath):
        raise ValueError('read() failed -- "{}"'.format(filepath))
    values = []
    for key in keys:
        values.append(parser.get(section, key))
    return values
        
