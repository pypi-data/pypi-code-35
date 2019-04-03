from drongo.client import DrongoClient


class NSClient(DrongoClient):
    def ns_create(self, name, description=None):
        data = {'name': name, 'description': description}
        response = self.post_json('/ns', data)
        if response['status'] == 'ERROR':
            return False, None
        else:
            return True, response['payload']

    def ns_activate(self, uid):
        response = self.get(
            '/ns/{uid}/operations/activate'.format(uid=uid))
        if response['status'] == 'ERROR':
            return False, None
        else:
            return True, response['payload']

    def ns_deactivate(self, uid):
        response = self.get(
            '/ns/{uid}/operations/deactivate'.format(uid=uid))
        if response['status'] == 'ERROR':
            return False, None
        else:
            return True, response['payload']

    def ns_get(self, uid):
        response = self.get('/ns/{uid}'.format(uid=uid))
        if response['status'] == 'ERROR':
            return False, None
        else:
            return True, response['payload']

    def ns_update(self, uid, name=None, description=None):
        data = {}
        if name is not None:
            data['name'] = name
        if description is not None:
            data['description'] = description

        response = self.put_json(
            '/ns/{uid}'.format(uid=uid),
            data)
        if response['status'] == 'ERROR':
            return False, None
        else:
            return True, response['payload']

    def ns_delete(self, uid):
        response = self.delete('/ns/{uid}'.format(uid=uid))
        if response['status'] == 'ERROR':
            return False, None
        else:
            return True, response['payload']

    def ns_list(self, active_only=True, page_number=1, page_size=50):
        params = {
            'active_only': 'yes' if active_only else 'no',
            'page_number': str(page_number),
            'page_size': str(page_size)
        }
        response = self.get('/ns', params=params)
        if response['status'] == 'ERROR':
            return False, None
        else:
            return True, response['payload']
