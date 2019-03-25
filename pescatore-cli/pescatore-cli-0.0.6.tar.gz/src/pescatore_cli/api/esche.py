from .commons import make_request


def list(page=None, items_per_page=None, **kwargs):
    params = {}

    if page:
        params['page'] = page
    if items_per_page:
        params['ipp'] = items_per_page

    return make_request(path='/api/v1/esche', params=params, **kwargs)


def create(body, **kwargs):
    params = {}

    return make_request(path='/api/v1/esche', params=params, payload=body,
                        method='POST', **kwargs)


def read(obj_id, **kwargs):
    params = {}

    return make_request(path='/api/v1/esche/{}'.format(obj_id), params=params,
                        **kwargs)


def delete(obj_id, **kwargs):
    params = {}

    return make_request(path='/api/v1/esche/{}'.format(obj_id), params=params,
                        method='DELETE', **kwargs)
