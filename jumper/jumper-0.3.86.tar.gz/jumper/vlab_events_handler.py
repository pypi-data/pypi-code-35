import json
import os
import sys
from .analytics import Analytics


class VlabEventsHandler:
    _EXAMPLES_HASH_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'examples_hash_list.json'))

    _analytics = None
    _local_jemu = False

    def __init__(self, web_api, local_jemu):
        self._analytics = Analytics(web_api, local_jemu)
        self._examples_hash_map = self._load_example_hash_map()

    def stop(self):
        self._analytics.stop()

    def add_event(self, message):
        if not self._local_jemu:
            self._analytics.add_event(message)

    def stop_after_event(self):
        self.add_event({
            'event': 'jumper run',
            'labels': {
                'parameter': 'stop_after'
            }
        })

    def start_run_event(self, firmware, new_signature, jemu_cmd):
        filename = os.path.basename(firmware)
        example_fw_name = self._get_example_fw_name(new_signature)
        sdk_cmd = 'jumper ' + ' '.join(sys.argv[1:])
        self.add_event({
            'event': 'start run from cli',
            "labels": {
                'Example Firmware': example_fw_name is not None,
                'Example Firmware Name': example_fw_name,
                'Firmware Name': filename,
                'sdk_cmd': sdk_cmd,
                'jemu_cmd': jemu_cmd,
                'Operating System': os.name
            }
        })

    def jumper_run_flags_event(self, args):
        self.add_event({'event': 'jumper run', 'labels': args})

    def error_event(self, labels):
        self.add_event({'event': 'error', 'labels': labels})

    def stop_run_event(self):
        self.add_event({'event': 'stop run'})

    def load_firmware_event(self, firmware_orig_name, new_signature):
        filename = os.path.basename(firmware_orig_name)
        if new_signature in self._examples_hash_map:
            self.add_event({
                'event': 'upload firmware',
                "labels": {
                    'example': True,
                    'example_name': self._examples_hash_map[new_signature],
                    'filename': filename
                }
            })
        else:
            self.add_event({
                'event': 'upload firmware',
                "labels": {
                    'example': False,
                    'filename': filename
                }
            })

    def _load_example_hash_map(self):
        try:
            return json.load(open(self._EXAMPLES_HASH_FILE))
        except Exception as e:
            print(e.message)
            return {}

    def _get_example_fw_name(self, new_signature):
        example_fw_name = None
        if new_signature in self._examples_hash_map:
            example_fw_name = self._examples_hash_map[new_signature]
        return example_fw_name
