import json

import six

from sdk.utils import hash_file
from .base import ReboticsBaseProvider, remote_service


class RetailerProvider(ReboticsBaseProvider):
    @remote_service('/api/v4/')
    def api_v4_root(self, session, **kwargs):
        return session.get()

    @remote_service('/api/v4/version/')
    def version(self, session, **kwargs):
        result = session.get()
        return result['version']

    @remote_service('/api/v4/token-auth/')
    def api_login(self, username, password):
        json_data = self.session.post(data={
            'username': username,
            'password': password
        })
        self.headers['Authorization'] = 'Token %s' % json_data['token']
        return json_data

    def get_token(self, username, password):
        response = self.api_login(username, password)
        return response['token']

    @remote_service('/api/v4/processing/actions/{id}/requeue/')
    def requeue(self, processing_action_id):
        return self.session.post(id=processing_action_id)

    @remote_service('/api/v4/processing/actions/{id}/')
    def processing_action_detail(self, processing_action_id):
        return self.session.get(id=processing_action_id)

    @remote_service('/api/v4/processing/actions/')
    def create_processing_action(
            self, store_id, files, input_type='image',
            store_planogram=None,
            aisle=None, section=None,
            klt_json=None, lens_used=None,
    ):
        for f_ in files:
            assert isinstance(f_, int), "Should send IDs of uploaded files"

        assert input_type in ('video', 'image', 'keyframe')

        data = {
            'store': store_id,
            'files': files,
            'input_type': input_type
        }
        if store_planogram:
            assert isinstance(store_planogram, int)
            data['store_planogram'] = store_planogram
        if aisle:
            assert isinstance(aisle, six.string_types)
            data['aisle'] = aisle
        if section:
            assert isinstance(section, six.string_types)
            data['section'] = section

        if klt_json:
            # encode KLT to string as it is accepted in API
            if isinstance(klt_json, dict):
                klt = json.dumps(klt_json)
            elif isinstance(klt_json, six.string_types):
                klt = klt_json
            else:
                # TODO: add path support and IO support
                raise ValueError('Unsupported value type for KLT.jsons')
            data['klt_json'] = klt

        if lens_used is not None:
            data['lens_used'] = lens_used
        return self.session.post(data=data)

    @remote_service('/api/v4/processing/upload/')
    def processing_upload(self, store_id, input_file, input_type='image'):
        assert isinstance(store_id, int), 'You need to specify store_id as int'
        assert input_type in (
            'image', 'video', 'keyframe'
        ), "File type should one of (image|video|keyframe) not %s" % input_type

        checksum = hash_file(input_file)
        input_file.seek(0)

        return self.session.post(data={
            'checksum': checksum,
            'input_type': input_type,
            'store': store_id
        }, files={
            'file': input_file
        })

    @remote_service('/api/v4/export/products/', timeout=30000)
    def export_products(self, products_filter=None):
        filter_params = {'filter': products_filter} if products_filter else None
        return self.session.get(params=filter_params)

    @remote_service('/api/v4/export/products/<product_id>/previews/')
    def get_product_previews(self, product_id, previews_filter=None):
        filter_params = {'filter': previews_filter} if previews_filter else None
        return self.session.get(
            url=self.session.host + '/api/v4/export/products/{}/previews/'.format(product_id),
            params=filter_params
        )

    @remote_service('/api/v4/export/products/previews/', timeout=30000)
    def get_product_previews_bulk(self, product_id_list):
        filter_params = {'id': product_id_list}
        return self.session.post(data=filter_params)
