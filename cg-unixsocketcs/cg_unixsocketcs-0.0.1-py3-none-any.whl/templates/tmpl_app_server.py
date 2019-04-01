from handler import Logic
from unixsocketcs.server import Server

if __name__ == "__main__":
    address = "{{ server_address }}"
    logic = Logic() 
    s = Server(address, logic)
    s.start()
