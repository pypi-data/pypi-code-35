from datetime import datetime, timezone
import socket
import os
import sys

from hawkei.version import VERSION
from hawkei.utils import merge, uuid, deep_compact
from hawkei.store import Store
from hawkei.config import config

_session_tracer_id = uuid()

def message_base():
    return ({
        'message_id': uuid(),
        'timestamp': datetime.utcnow().replace(tzinfo=timezone.utc).isoformat(),
        'session_tracker_id': _session_tracer_id,
    })

def message_extended():
    message = merge({
        'library': _library(),
        'server': _server(),
        'environment': config.data.get('environment_name'),
        'metadata': config.data.get('metadata'),
    }, message_base())

    message = merge(message, Store.get())

    return deep_compact(message)

def _library():
    return ({
        'name': 'hawkei',
        'language': 'python',
        'version': VERSION,
    })

def _server():
    return {
        'host': socket.gethostname(),
        'pid': os.getpid(),
        'software': Store.get().get('software') or sys.argv[0] or 'unknown',
    }
