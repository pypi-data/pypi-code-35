import json
import logging
import re

from .base import ReboticsBaseProvider, remote_service

logger = logging.getLogger(__name__)

# FIXME: why are we doing the RPC stuff through REST API?


class DatasetProvider(ReboticsBaseProvider):
    @remote_service('/api/v1/')
    def api_root(self):
        return self.session.get()

    @remote_service('/api/v1/')
    def classify(self, **kwargs):
        pass

    @remote_service('/api/v1/classifications/reference-codes/batch/')
    def save_feature_vector_batch(self, data):
        return self.session.post(json=json.dumps(list(data)))

    @remote_service('/api/v1/classifications/reference-codes/')
    def save_feature_vector_single(self, data):
        return self.session.post(data=data)

    def inject_retailer_reference(self, data, retailer):
        if 'x-retailer-id' not in self.get_authentication_headers().keys():
            if retailer is None:
                raise ValueError('You need to specify retailer '
                                 'if you are not using retailer-in-admin authentication')
            data['retailer'] = retailer.strip()
        return data

    def construct_reference_entry(self, upc, feature, retailer, facenet):
        data = {
            'upc': upc.strip(),
            'feature': feature.strip(),
            'facenet': facenet.strip()
        }

        self.inject_retailer_reference(data, retailer)
        return data

    def save_feature_vector(self, upc, facenet, feature, retailer=None, batch_size=1):
        if batch_size > 1:
            data_to_post = [
                self.construct_reference_entry(upc=upc_code, feature=feature_vector, retailer=retailer, facenet=facenet)
                for upc_code, feature_vector in zip(upc, feature)
            ]
            result = []
            for batch_index in range(0, len(data_to_post), batch_size):
                result.append(self.save_feature_vector_batch(data_to_post[batch_index:batch_index + batch_size]))
            return result
        return self.save_feature_vector_single(data=self.construct_reference_entry(upc, feature, retailer, facenet))

    @remote_service('/api/v1/classifications/reference-codes/delete/')
    def delete_feature_vector(self, upc, facenet_version, feature):
        json_data = self.session.post(data={
            'upc': upc,
            'facenet': facenet_version,
            'feature': feature,
        })
        return json_data

    @remote_service('/api/v1/classifications/reference-codes/')
    def delete_feature_vector_by_id(self, object_id):
        response = self.session.delete(object_id)
        logger.debug('Deleted: %s', response)
        return response

    @remote_service('/api/v1/token-auth/')
    def token_auth(self, username, password):
        json_data = self.session.post(data=dict(
            username=username,
            password=password
        ))
        self.headers['Authorization'] = 'Token %s' % json_data['token']
        return json_data

    @remote_service('/api/v1/classifications/reference-codes/backup/', raw=True)
    def download_reference_database(self, retailer, facenet):
        response = self.session.post(data=dict(
            retailer=retailer,
            facenet=facenet,
        ), stream=True)
        filename = re.findall("filename=(.+)", response.headers['content-disposition'])[0].strip('"')
        return filename, response.raw

    @remote_service('/api/v1/retailer/settings/features/limit/')
    def set_feature_limit_for_product(self, limit, upc, retailer=None):
        data = dict(
            upc=upc,
            limit=limit
        )
        self.inject_retailer_reference(data, retailer)
        response = self.session.post(data=data)
        return response

    @remote_service('/api/v1/retailer/settings/')
    def set_settings(self, data, retailer=None):
        data = self.inject_retailer_reference(data, retailer)
        response = self.session.post(data=data)
        return response

    @remote_service('/api/v1/check_feature_vector_exists/', timeout=300000)
    def test_feature_vector_existence_bulk(self, data, retailer=None):
        data = self.inject_retailer_reference(data, retailer)
        response = self.session.post(json=data)
        return response
