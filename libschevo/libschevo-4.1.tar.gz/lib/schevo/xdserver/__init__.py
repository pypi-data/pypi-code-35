from .server import Server

def make_server(path, host='127.0.0.1', port=22972, serverClass=Server):
    server = serverClass(path, host=host, port=port)
    return server
