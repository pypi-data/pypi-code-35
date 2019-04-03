"""
hudai.resources.model_score
"""
from ..helpers.resource import Resource


class ModelScoreResource(Resource):
    def __init__(self, client):
        Resource.__init__(self, client, base_path='/articles/scores')
        self.resource_name = 'ModelScore'

    def list(self,
             article_id=None,
             model=None,
             ):
        return self._list(
            article_id=article_id,
            model=model,
        )

    def create(self,
               article_id=None,
               model_id=None,
               model_name=None,
               model_score=None,
               model_version=None,
               model_url=None,
               data_url=None,
               ):
        return self._create(
            article_id=article_id,
            model_id=model_id,
            model_name=model_name,
            model_score=model_score,
            model_version=model_version,
            model_url=model_url,
            data_url=data_url,
        )

    def fetch(self, entity_id):
        return self._fetch(entity_id)

    def upsert(self,
               article_id=None,
               model_id=None,
               model_name=None,
               model_score=None,
               model_version=None,
               model_url=None,
               data_url=None,
               ):
        return self._upsert(
            article_id=article_id,
            model_id=model_id,
            model_name=model_name,
            model_score=model_score,
            model_version=model_version,
            model_url=model_url,
            data_url=data_url,
        )

    def delete(self, entity_id):
        return self._delete(entity_id)
