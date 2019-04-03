"""
hudai.resources.article_geography
"""
from ..helpers.resource import Resource


class ArticleGeographyResource(Resource):
    def __init__(self, client):
        Resource.__init__(self, client, base_path='/articles/{article_id}/geographies')
        self.resource_name = 'ArticleGeography'

    def list(self, article_id, page=None):
        query_params = self._set_limit_offset({'page': page})

        return self.http_get('/', params={'article_id': article_id},
                                  query_params=query_params)

    def create(self, article_id, geography):
        return self.http_post('/', params={'article_id': article_id},
                                   data={'geography': geography})

    def fetch(self, article_id, geography):
        return self.http_get('/{geography}',
                             params={'article_id': article_id, 'geography': geography})

    def delete(self, article_id, geography):
        return self.http_delete('/{geography}',
                                params={'article_id': article_id, 'geography': geography})
