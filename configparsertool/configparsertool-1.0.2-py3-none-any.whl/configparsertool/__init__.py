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
        

def getdict(filepath, section, keys):
    parser = configparser.ConfigParser()
    if not parser.read(filepath):
        raise ValueError('read() failed -- "{}"'.format(filepath))
    table = {}
    for key in keys:
        table[key] = parser.get(section, key)
    return table
