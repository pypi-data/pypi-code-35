import threading
import time
import ipywidgets as widgets
import sys

output_registry = {}
active_callbacks = set()

def callback_active():
    return threading.currentThread().name in active_callbacks

class OutputRedirector:
    def __init__(self, original):
        self.original = original
    
    def write(self, msg):
        thread_name = threading.currentThread().name
        if thread_name != 'MainThread':
            output_registry[threading.currentThread().getName()].append_stdout(msg)
        else:
            self.original.write(msg)
            
    def flush(self):
        self.original.flush()

sys.stdout = Outer(sys.stdout)

def threader():
    out = widgets.Output(layout={'border': '1px solid black'})
    my_thread = threading.Thread(target=doubler, args=(2,))
    name = my_thread.getName()
    active_callbacks.add(name)
    output_registry[name] = out
    
    my_thread.start()
    
    btn = widgets.Button(description="Stop")
    btn.on_click(lambda x: active_callbacks.remove(name))
    vbox = widgets.VBox((btn, out))
    return vbox


def subscribe(topic, msg_type, callback):
	"""
	Subscribes to a specific topic in another thread, but redirects output!
	
	@param topic The topic
	@param msg_type The message type
	@param callback The callback
	
	@return Jupyter output widget
	"""

    out = widgets.Output(layout={'border': '1px solid black'})
    my_thread = threading.Thread(target=doubler, args=(2,))
    name = my_thread.getName()
    active_callbacks.add(name)
    output_registry[name] = out
    
    my_thread.start()
    
    btn = widgets.Button(description="Stop")
    btn.on_click(lambda x: active_callbacks.remove(name))
    vbox = widgets.VBox((btn, out))
    return vbox


	