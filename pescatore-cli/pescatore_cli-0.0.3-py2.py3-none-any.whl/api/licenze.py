from .commons import make_request


def list(page=None, items_per_page=None):
    params = {}

    if page:
        params['page'] = page
    if items_per_page:
        params['ipp'] = items_per_page

    return make_request(path='/api/v1/licenze', params=params)

def create(**kwargs):
    params = {}

    return make_request(path='/api/v1/licenze', params=params, payload=kwargs,
                        method='POST')

def read(obj_id):
    params = {}

    return make_request(path='/api/v1/licenze/{}'.format(obj_id), params=params)

def delete(obj_id):
    params = {}

    return make_request(path='/api/v1/licenze/{}'.format(obj_id), params=params,
                        method='DELETE')
