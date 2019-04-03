from drongo.client import DrongoClient


class SettingsClient(DrongoClient):
    def settings_set(self, mod, settings):
        response = self.put_json('/settings/{mod}'.format(mod=mod), settings)
        if response['status'] == 'ERROR':
            return False, None
        else:
            return True, response['payload']

    def settings_get(self, mod):
        response = self.get('/settings/{mod}'.format(mod=mod))
        if response['status'] == 'ERROR':
            return False, None
        else:
            return True, response['payload']
