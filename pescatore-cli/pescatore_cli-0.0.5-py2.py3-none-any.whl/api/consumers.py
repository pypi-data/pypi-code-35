from .commons import make_request


def list(page=None, items_per_page=None):
    params = {}

    if page:
        params['page'] = page
    if items_per_page:
        params['ipp'] = items_per_page

    return make_request(path='/api/v1/consumers', params=params)

def read(obj_id):
    params = {}

    return make_request(path='/api/v1/consumers/{}'.format(obj_id), params=params)
