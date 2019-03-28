# -*- coding: utf-8 -*-
import pytest
from unittest import TestCase
from elastic_lib import ElasticFactory, DictFactory, ElasticModel


class ElasticTestModel(ElasticModel):
  """"""
  # put reserve at begining to be make it work with the template
  ELASTIC_INDEX_PREFIX = 'lib_test_'

  @classmethod
  def get_connection(cls):
    """Overwrite to set a connection."""
    import os
    import elasticsearch
    elastic_server = os.environ.get('ELASTIC_SERVER', None)
    return elasticsearch.Elasticsearch(elastic_server)


class DummyEs(ElasticTestModel):
  """Dummy elastic index to persiste data."""
  __index_name__ = 'banana'


class DummyElasticFactory(ElasticFactory):
  """Dummy factory."""
  class Meta:
    model = DummyEs

  id = 1
  name = 'Banana'


class DummyDictFactory(DictFactory):
  """Dummy factory."""
  id = 1
  name = 'Banana'


class UtilsTest(TestCase):
  """Test for the utils."""

  def test_dict_factory(self):
    """Usage call for the dict factory."""
    # build a dummy dictFactory with attributs

    # you cannot call this way as the default init call create whitch persiste the data in db
    with pytest.raises(NotImplementedError):
      factory = DummyDictFactory()

    # validate that default call work same way than create
    with pytest.raises(NotImplementedError):
      factory = DummyDictFactory.create()

    factory = DummyDictFactory.build()
    # check that we can acess data as dict
    self.assertEqual(factory.get('id'), 1)
    self.assertEqual(factory.get('name'), 'Banana')

    # overwite some values
    new_factory = DummyDictFactory.build(id=5, name='Orange')
    self.assertEqual(new_factory.get('id'), 5)
    self.assertEqual(new_factory.get('name'), 'Orange')

  def test_elastic_factory_usage(self):
    """Usage call for the elastic factory."""
    factory_es = DummyElasticFactory()
    # the factory_es object can be accessed as dict and object for the init version
    self.assertEqual(factory_es.get('id'), 1)
    self.assertEqual(factory_es.get('name'), 'Banana')
    # you access the default values when call attributs
    self.assertEqual(factory_es.id, 1)
    self.assertEqual(factory_es.name, 'Banana')

    # the object is persisted in elastic
    dummy_es = DummyEs.get_by_id(1)
    self.assertEqual(dummy_es.get('id'), 1)
    self.assertEqual(dummy_es.get('name'), 'Banana')

    # here we have a dict as elastic result
    with pytest.raises(AttributeError):
      self.assertEqual(dummy_es.id)

  def test_elastic_factory_overwite(self):
    """Overwrite the data for the elastic factory."""
    # Overwrite data
    factory_es = DummyElasticFactory(id=1, name='Pineapple')
    # the factory object is updated
    self.assertEqual(factory_es.get('name'), 'Pineapple')

    # but attributs are not overwritten
    self.assertEqual(factory_es.name, 'Banana')

    # the data are saved in elastic
    dummy_es = DummyEs.get_by_id(1)
    self.assertEqual(dummy_es.get('name'), 'Pineapple')

  def test_elastic_factory_limitation(self):
    """Limitation for the elastic factory."""
    factory_es = DummyElasticFactory()

    # Limitations
    factory_es.name = 'Orange'
    # updating attribut don't persiste or update the dict
    self.assertEqual(factory_es.name, 'Orange')
    self.assertEqual(factory_es.get('name'), 'Banana')

    dummy_es = DummyEs.get_by_id(1)
    self.assertEqual(dummy_es.get('name'), 'Banana')
