# -*- coding: utf-8 -*-
from unittest import TestCase
from elastic_lib import ElasticModel, ElasticPeriod, ElasticSequence


class ElasticTest(object):
  """Meta model to build the connection."""

  @classmethod
  def get_connection(cls):
    """Overwrite to set a connection."""
    import os
    import elasticsearch
    elastic_server = os.environ.get('ELASTIC_SERVER', None)
    return elasticsearch.Elasticsearch(elastic_server)


class ElasticTestModel(ElasticTest, ElasticModel):
  """"""
  # put reserve at begining to be make it work with the template
  ELASTIC_INDEX_PREFIX = 'lib_test_'


class ElasticTestPeriod(ElasticTest, ElasticPeriod):
  """"""

  INDEX_PREFIX = 'lib_test_period_'


class ElasticTestSequence(ElasticTest, ElasticSequence):
  """"""
  INDEX_PREFIX = 'lib_test_'


class ModelElasticEsTest(TestCase):
  """Super class for all the search in ElasticTestModel."""

  use_elastic = True

  def setUp(self):
    """."""
    super(ModelElasticEsTest, self).setUp()

  def tearDown(self):
    """."""
    # remove all the test indices
    conn = ElasticTestModel.get_connection()
    conn.indices.delete(index='%s*' % ElasticTestModel.ELASTIC_INDEX_PREFIX)
    # and sequence
    conn.indices.delete(index='%s%s*' % (ElasticTestSequence.ELASTIC_INDEX_PREFIX, ElasticTestSequence.INDEX_PREFIX))
    super(ModelElasticEsTest, self).tearDown()

  def test_process_search_query_page_limit(self):
    """Check that the page and limit are not lost."""
    ElasticTestModel.__index_name__ = '1'

    res = ElasticTestModel.process_search_query(search_params=None, regular_term_fields=[], regular_terms_fields=[], regular_date_fields=[], post_params=None, aggs=None, sort=None, page=35, limit=12, render='query')

    # from must be 408 (35*12) -12
    self.assertEqual(res['from'], 408)
    self.assertEqual(res['size'], 12)

  def test_process_search_query_aggs_simple(self):
    """One example using simple terms aggregations with formatted result."""
    ElasticTestModel.__index_name__ = '55'

    # put some dummy data
    for x in range(0, 3):
      ElasticTestModel.save({'team': 'Tomato'})
    for x in range(0, 5):
      ElasticTestModel.save({'team': 'Banana'})
    for x in range(0, 2):
      ElasticTestModel.save({'team': 'Potatoes'})

    ElasticTestModel.refresh()

    aggs = {'TEAM': {'terms': {'field': 'team.keyword'}}}

    res = ElasticTestModel.process_search_query(search_params=None, regular_term_fields=[], regular_terms_fields=[], regular_date_fields=[], post_params=None, aggs=aggs, sort={'team.keyword': 'asc'}, limit=0, page=1)

    # put the result in a list to confirm the order
    res_list = [(team_name, total) for team_name, total in res['aggs']['TEAM'].items()]

    # first record is the one with more records
    self.assertEqual(res_list[0][0], 'Banana')
    self.assertEqual(res_list[0][1], 5)
    # second tomato
    self.assertEqual(res_list[1][0], 'Tomato')
    self.assertEqual(res_list[1][1], 3)
    # last potatoes
    self.assertEqual(res_list[2][0], 'Potatoes')
    self.assertEqual(res_list[2][1], 2)

    # total of ducment is correctly returned
    self.assertEqual(res['total'], 10)

  def test_process_search_query_fields_list(self):
    """Test that we can ask for specific fields in list format."""
    self._dummy_data()

    res = ElasticTestModel.process_search_query(search_params=None, regular_term_fields=[], regular_terms_fields=[], regular_date_fields=[], post_params=None, aggs=None, sort={'team.keyword': 'asc'}, limit=10, page=1, fields=['id', 'name'], render='pager')
    # check that we don't have team we only ask id and name
    for one_result in res[ElasticTestModel.get_index_name()]:
      for one_field in one_result.keys():
        self.assertIn(one_field, ['id', 'name'])
        self.assertNotEqual(one_field, 'team')

    res = ElasticTestModel.process_search_query(search_params=None, regular_term_fields=[], regular_terms_fields=[], regular_date_fields=[], post_params=None, aggs=None, sort={'team.keyword': 'asc'}, limit=10, page=1, fields=['team'], render='pager')
    # it always return the id even if we don't ask and we have team but not name
    for one_result in res[ElasticTestModel.get_index_name()]:
      for one_field in one_result.keys():
        self.assertIn(one_field, ['id', 'team'])
        self.assertNotEqual(one_field, 'name')

  def test_process_search_query_fields_string(self):
    """Test that we can ask for specific fields in string format."""
    self._dummy_data()

    res = ElasticTestModel.process_search_query(search_params=None, regular_term_fields=[], regular_terms_fields=[], regular_date_fields=[], post_params=None, aggs=None, sort={'team.keyword': 'asc'}, limit=10, page=1, fields='name', render='pager')
    # check that we don't have team we only ask id and name
    for one_result in res[ElasticTestModel.get_index_name()]:
      for one_field in one_result.keys():
        self.assertIn(one_field, ['id', 'name'])
        self.assertNotEqual(one_field, 'team')

  def test_process_search_query_paginator_with_aggs(self):
    """"Check that we can use paginator render with aggregations."""
    # insert dummy data
    self._dummy_data()
    aggs = {'team': {'terms': {'field': 'team.keyword'}}}
    result = ElasticTestModel.process_search_query(search_params=None, regular_term_fields=[], regular_terms_fields=[], regular_date_fields=[], post_params=None, aggs=aggs, sort={'team.keyword': 'asc'}, limit=10, page=1, render='paginator')
    self.assertTrue(result['aggs']['team'])
    self.assertEqual(result['total'], 2)
    paginate, page_data = result[ElasticTestModel.get_index_name()]
    self.assertEqual(page_data['total'], 2)
    from django.core.paginator import Page
    self.assertTrue(isinstance(paginate, Page))

  def _dummy_data(self):
    """Push some dummy data."""

    ElasticTestModel.__index_name__ = '123'

    ElasticTestModel.save({'team': 'Tomato', 'id': 11, 'name': 'Anton'})
    ElasticTestModel.save({'team': 'Tornado', 'id': 15, 'name': 'Soul'})
    ElasticTestModel.refresh()

  def test_render_paginator(self):
    """Test that the render return correct format."""
    ElasticTestModel.__index_name__ = '1'
    # need to create the index
    from django.core.paginator import Page
    conn = ElasticTestModel.get_connection()
    conn.indices.create(ElasticTestModel.get_index_name())
    # we don't have document we just check the strucutre
    query = {'query': {'match_all': {}}}
    result = ElasticTestModel.search(query)
    result = ElasticTestModel.render_paginator(result)
    # the render return a list (with paginated data and a dict for the pagination) and total
    assert result[1] == 0
    paginated_data, pages_data = result[0]
    # check some keys we have in pages data
    assert 'page_range' in pages_data
    assert 'total' in pages_data
    self.assertEqual(pages_data['total'], 0)
    assert 'item_start' in pages_data
    assert 'item_end' in pages_data

    # the paginated data is an instance of Page from paginator
    assert isinstance(paginated_data, Page)

  def test_render_select_default(self):
    """Test that the render select is working correctly and return beautyfull select lists."""
    self._dummy_data()
    result = ElasticTestModel.search({'query': {'match_all': {}}})
    select_rendered = ElasticTestModel.render_select(result)

    # we know the dummy data so we expect this result
    dummy_data_keys = [11, 15]
    dummy_data_names = ['Anton', 'Soul']
    self.assertEqual(len(select_rendered), 2)
    for one_result in select_rendered:
      self.assertIn(one_result[0], dummy_data_keys)
      self.assertIn(one_result[1], dummy_data_names)

  def test_render_select_with_constants(self):
    """Check that settings constant will return the expected result."""
    self._dummy_data()
    # set the constants fields
    ElasticTestModel.KEYWORD_FIELD = 'team'
    ElasticTestModel.ID_KEY = '_id' # it's actually the same as id as we set id but it will be string

    result = ElasticTestModel.search({'query': {'match_all': {}}})
    select_rendered = ElasticTestModel.render_select(result)
    # we know the dummy data so we expect this result
    dummy_data_keys = ['11', '15']
    dummy_data_fields = ['Tornado', 'Tomato']
    self.assertEqual(len(select_rendered), 2)
    for one_result in select_rendered:
      self.assertIn(one_result[0], dummy_data_keys)
      self.assertIn(one_result[1], dummy_data_fields)

  def test_render_select_with_defined(self):
    """Check that we can overwrite the select fields if we want something specific."""
    self._dummy_data()
    result = ElasticTestModel.search({'query': {'match_all': {}}})
    select_rendered = ElasticTestModel.render_select(result, fields=('name', 'team'))
    dummy_data_names = ['Anton', 'Soul']
    dummy_data_fields = ['Tornado', 'Tomato']
    self.assertEqual(len(select_rendered), 2)
    for one_result in select_rendered:
      self.assertIn(one_result[0], dummy_data_names)
      self.assertIn(one_result[1], dummy_data_fields)

  def test_msearch_with_header(self):
    """Test that the msearch with a header get the correct result."""
    index_1 = '1'
    index_2 = '2'
    index_all = '*'
    full_index_1 = '%s%s' % (ElasticTestModel.ELASTIC_INDEX_PREFIX, index_1)
    full_index_2 = '%s%s' % (ElasticTestModel.ELASTIC_INDEX_PREFIX, index_2)
    full_index_all = '%s%s' % (ElasticTestModel.ELASTIC_INDEX_PREFIX, index_all)
    ElasticTestModel.__index_name__ = index_1
    ElasticTestModel.save({'id': 1, 'foo': 'bar', 'foo2': []})
    ElasticTestModel.save({'id': 2, 'foo': 'bar', 'foo2': ['bar']})
    ElasticTestModel._refresh(full_index_1)
    ElasticTestModel.__index_name__ = index_2
    ElasticTestModel.save({'id': 1, 'foo': 'babar', 'foo2': []})
    ElasticTestModel.save({'id': 2, 'foo': 'babar', 'foo2': ['bar']})
    ElasticTestModel._refresh(full_index_2)

    queries = [
      {'query': {'term': {'id': 1}}},
      {'query': {'term': {'id': 2}}},
      {'query': {'match_all': {}}}
    ]

    keys = ['from_lambda1', 'from_lambda2', 'from both']
    header = [{'index_name': full_index_1}, {'index_name': full_index_2}, {'index_name': full_index_all}]

    result = ElasticTestModel.msearch(queries, keys, header)

    # only one result here
    assert result['from_lambda1']['total'] == 1
    assert result['from_lambda1'][full_index_1]['%s_1' % full_index_1]['foo'] == u'bar'
    assert result['from_lambda2']['total'] == 1
    assert result['from_lambda2'][full_index_2]['%s_2' % full_index_2]['foo2'] == ['bar']
    # here the 4 docs
    result['from both']['total'] == 4
    counter = 0
    for idx, one_result in result['from both'][full_index_all].items():
      assert one_result.get('id') in (1, 2)
      counter += 1
    # check that the ids didn't merge
    assert result['from both']['total'] == counter

  def test_msearch_with_error(self):
    """Test that the malformed data raise."""
    # list have not the same size
    self.assertRaises(AssertionError, lambda: ElasticTestModel.msearch([1, 2, 3], [1]))
    self.assertRaises(AssertionError, lambda: ElasticTestModel.msearch([1, 2, 3], [1, 2, 3], [1]))

    # not error but empty result index not exist
    ElasticTestModel.__index_name__ = u'1'
    result = ElasticTestModel.msearch([{'query': {'match_all': {}}}], ['A'])
    assert result['A']['total'] == 0

    # check when there's error in the query that it raise an error
    from elasticsearch.exceptions import TransportError
    self.assertRaises(TransportError, lambda: ElasticTestModel.msearch([{'query': {'not_existing_thing': {}}}], ['A']))

  def test_msearch(self):
    """Test that the msearch return the correct things, in the corect order."""
    ElasticTestModel.__index_name__ = '1'
    full_index_name = '%s%s' % (ElasticTestModel.ELASTIC_INDEX_PREFIX, ElasticTestModel.__index_name__)
    ElasticTestModel.save({'id': 1, 'foo': 'bar', 'foo2': []})
    ElasticTestModel.save({'id': 2, 'foo': 'bar2', 'foo2': ['bar']})
    ElasticTestModel.refresh()

    queries = [
      {'query': {'term': {'id': 1}}},
      {'query': {'term': {'id': 2}}}
    ]
    keys = ['first_foo_bar', 'second_foo_bar']

    result = ElasticTestModel.msearch(queries, keys)

    # we have only one result here
    assert result['first_foo_bar']['total'] == 1
    assert result['first_foo_bar'][full_index_name]['%s_1' % full_index_name]['id'] == 1
    assert result['second_foo_bar'][full_index_name]['%s_2' % full_index_name]['foo'] == u'bar2'

  def test_count(self):
    """Test that the count return the correct number of result."""
    ElasticTestModel.__index_name__ = '1'
    ElasticTestModel.save({'id': 1, 'foo': 'bar', 'foo2': []})
    ElasticTestModel.save({'id': 2, 'foo': 'bar2', 'foo2': ['bar']})
    ElasticTestModel.refresh()

    # default count make a match all
    assert ElasticTestModel.count() == 2
    # we can filter by query
    assert ElasticTestModel.count(query={'query': {'term': {'id': 1}}}) == 1
    # check that forcing the size change nothing ex: we use a generic call that set a size
    assert ElasticTestModel.count(query={'query': {'term': {'id': 1}}, 'size': 102}) == 1

    ElasticTestModel.__index_name__ = '2'
    ElasticTestModel.save({'id': 1, 'foo': 'bar', 'foo2': []})
    ElasticTestModel.save({'id': 2, 'foo': 'bar2', 'foo2': ['bar']})
    ElasticTestModel.refresh()

    # check for several indices
    multi_index = '%s*' % ElasticTestModel.ELASTIC_INDEX_PREFIX
    assert ElasticTestModel.count(myindex=multi_index) == 4
    # and with query
    assert ElasticTestModel.count(query={'query': {'term': {'id': 1}}}, myindex=multi_index) == 2

  def test_process_search_query_raw_search(self):
    """Test that the search with raw search perform corectly."""
    ElasticTestModel.__index_name__ = '1'
    ElasticTestModel.save({'id': 1, 'foo': 'bar', 'foo2': []})
    ElasticTestModel.save({'id': 2, 'foo': 'bar2', 'foo2': ['bar']})
    ElasticTestModel.refresh()

    raw_search = {'exists': {'field': 'foo2'}}
    sort = 'id'

    result = ElasticTestModel.process_search_query(search_params={'foo': 'bar'}, regular_term_fields=['foo'], regular_terms_fields=[], regular_date_fields=[], post_params=[], aggs={}, sort=sort, page=1, limit=10, raw_search=raw_search)
    assert result['total'] == 0

    result = ElasticTestModel.process_search_query(search_params={'foo': 'bar2'}, regular_term_fields=['foo'], regular_terms_fields=[], regular_date_fields=[], post_params=[], aggs={}, sort=sort, page=1, limit=10, raw_search=raw_search)
    assert result['total'] == 1

    for idx, one_result in result[ElasticTestModel.get_index_name()].items():
      assert idx == 2

    # search for the other one
    raw_search = {'bool': {'must_not': raw_search}}

    result = ElasticTestModel.process_search_query(search_params={'foo': 'bar'}, regular_term_fields=['foo'], regular_terms_fields=[], regular_date_fields=[], post_params=[], aggs={}, sort=sort, page=1, limit=10, **{'raw_search': raw_search})

    assert result['total'] == 1
    for idx, one_result in result[ElasticTestModel.get_index_name()].items():
      assert idx == 1

  def test_process_search_query_no_source(self):
    """Test that the option no_source return the data with the correct format."""
    ElasticTestModel.__index_name__ = '1'
    ElasticTestModel.save({'id': 1, 'foo': 'bar'})
    ElasticTestModel.save({'id': 2, 'foo': 'bar2'})
    ElasticTestModel.refresh()
    sort = 'id'
    result = ElasticTestModel.process_search_query(search_params={'foo': 'bar'}, regular_term_fields=['foo'], regular_terms_fields=[], regular_date_fields=[], post_params=[], aggs={}, sort=sort, page=1, limit=10, **{'no_source': True})

    for one_result in result[ElasticTestModel.get_index_name()]['hits']['hits']:
      # we'll don't have _source
      self.assertRaises(KeyError, lambda: one_result['_source'])

  def test_process_filters(self):
    """Check that the query is correctly built when we provide a filter."""
    regular_term_fields = ['status']
    ElasticTestModel.__index_name__ = '1'
    conn = ElasticTestModel.get_connection()
    # need to create the index before validating the query
    conn.indices.create(ElasticTestModel.get_index_name())
    query = {}
    filters = ElasticTestModel.process_regular_fields(search_params={'status': 'Private'}, regular_term_fields=regular_term_fields, regular_terms_fields=[], regular_date_fields=[])
    result_query = ElasticTestModel.process_filters(query, filters)
    assert result_query == {'bool': {'must': [{'bool': {'must': [{'term': {'status': 'Private'}}]}}]}}
    # validate the syntax
    validation = ElasticTestModel.validate_query({'query': result_query})
    assert validation['valid'] is True

  def test_process_keyword_query_filter(self):
    """Check that the query is correctly built when we provide a keyword."""

    ElasticTestModel.FORCE_ANALYZER = 'whitespace' # set teh default analyzer as we are naked here!
    regular_term_fields = ['status']
    ElasticTestModel.__index_name__ = '1'
    conn = ElasticTestModel.get_connection()
    # need to create the index before validating the query
    conn.indices.create(ElasticTestModel.get_index_name())
    query = {}
    filters = ElasticTestModel.process_regular_fields(search_params={'status': 'Private'}, regular_term_fields=regular_term_fields, regular_terms_fields=[], regular_date_fields=[])
    filter_query = ElasticTestModel.process_filters(query, filters)

    filter_parts = filter_query['bool']['must'][0]

    query, keyword_query = ElasticTestModel.process_keyword_query_filter(filter_query, search_params={'keyword': u'banana'})

    # check that the filter is still here
    assert query['bool']['must'][0] == filter_parts
    validation = ElasticTestModel.validate_query({'query': query})
    assert validation['valid'] is True

  def test_clean_keyword(self):
    """Clean keyword search.

    remove some unwanted char keyword sent to Elastic search.

    """
    assert ElasticTestModel.clean_keyword(u"lorem ipsum") == u"lorem ipsum" # romaji
    assert ElasticTestModel.clean_keyword(u"lorem_ipsum") == u"lorem_ipsum" # romaji w/ underscore
    assert ElasticTestModel.clean_keyword(u"2pacs") == u"2pacs"
    assert ElasticTestModel.clean_keyword(u"contest2") == u"contest2"
    assert ElasticTestModel.clean_keyword(u"#cat") == u"#cat" # romaji w/ sharp(u0024) elastic ignore it so no need to remove
    assert ElasticTestModel.clean_keyword(u"ファッションラテ") == u"ファッションラテ"
    assert ElasticTestModel.clean_keyword(u"かしこまりました") == u"かしこまりました"
    assert ElasticTestModel.clean_keyword(u"神奈川県川崎市川崎区") == u"神奈川県川崎市川崎区"
    assert ElasticTestModel.clean_keyword(u"LXall 情報共有 (★社員専用)") == u"lxall 情報共有 \\(社員専用\\)"  # mix romaji + kanji + star

    assert ElasticTestModel.clean_keyword(u"頑張ります！") == u"頑張ります！" # kanji + hiragana
    assert ElasticTestModel.clean_keyword(u"Mickey 🐭") == u"mickey" # romaji + emoji
    # apply filter
    assert ElasticTestModel.clean_keyword(u"LXall 情報共有 ★社員専用", "romaji") == u"lxall" # keep only romaji
    assert ElasticTestModel.clean_keyword(u"LXall 情報共有 (★社員専用)", "romaji") == u"lxall \\(\\)" # same w/ ()
    assert ElasticTestModel.clean_keyword(u"頑張ります！", "kanji") == u"頑張"
    assert ElasticTestModel.clean_keyword(u"笑顔1", "kanji") == u"笑顔"
    assert ElasticTestModel.clean_keyword(u"頑張ります！", "hiragana") == u"ります"

    assert ElasticTestModel.clean_keyword(u"ファッションです。", "katakana") == u"ファッション"
    assert ElasticTestModel.clean_keyword(u"ファッションです。", "punctuation") == u"。"
    assert ElasticTestModel.clean_keyword(u"ﾈｺです。=ｃａｔ", "fw_r_hw_k") == u"ﾈｺｃａｔ"
    assert ElasticTestModel.clean_keyword(u"ef/l") == u"ef\\/l" # reference find for lens
    assert ElasticTestModel.clean_keyword(u"----") == u"\-\-\-\-" # reference find for lens
    assert ElasticTestModel.clean_keyword(u'sa"*') == u'sa\\\"*' # error found in logs

  def test_mget_list_id(self):
    """Test the mget with list of ids."""
    ElasticTestModel.__index_name__ = '1'
    ElasticTestModel.save({'id': 1, 'foo': 'bar'})
    ElasticTestModel.save({'id': 2, 'foo': 'bar2'})
    ElasticTestModel.save({'id': 3, 'foo': 'bar3'})

    list_ids = [1, 2, 3]
    result = ElasticTestModel.mget(list_ids)
    assert result['total'] == 3
    for idx, one_doc in result[ElasticTestModel.get_index_name()].items():
      assert one_doc['id'] in list_ids

  def test_from_limit(self):
    """Test the limit option for the search from."""
    # add some data
    ElasticTestModel.__index_name__ = '1'
    ElasticTestModel.save({'id': 1, 'foo': 'bar'})
    ElasticTestModel.save({'id': 2, 'foo': 'bar2'})
    ElasticTestModel.save({'id': 3, 'foo': 'bar3'})
    ElasticTestModel.refresh()
    # asking for the last (third) one
    result, total = ElasticTestModel.search({'from': 2, 'sort': 'id', 'size': 1}, pager=True)
    # we don't filter so get total of all results

    assert total == 3
    # we get bar2
    assert result[0]['foo'] == 'bar3'
    # override the limit
    original_value = ElasticTestModel.MAX_FROM_FOR_PAGINATION
    ElasticTestModel.MAX_FROM_FOR_PAGINATION = 1
    # asking for the last (third) one
    result, total = ElasticTestModel.search({'from': 2, 'sort': 'id', 'size': 1}, pager=True)
    # we can't get over the limit
    assert result[0]['foo'] == 'bar2'
    # put back the original value for the other tests
    ElasticTestModel.MAX_FROM_FOR_PAGINATION = original_value

  def test_aggregation_select(self):
    """Test the generation of list for select box from a field name."""
    ElasticTestModel.__index_name__ = '1'
    # set a mapping to have an untouched field
    conn = ElasticTestModel.get_connection()
    # need to create the index before assigning a mapping
    print('index_create: ', ElasticTestModel.get_index_name())
    conn.indices.create(ElasticTestModel.get_index_name())
    conn.indices.put_mapping(
      index=ElasticTestModel.get_index_name(),
      doc_type=ElasticTestModel.__doc_type__,
      body={
        ElasticTestModel.__doc_type__: {
          "properties": {
            "city": {
              "type": "text",
              "fields": {
                "untouched": {
                  "type": "keyword"
                }
              }
            }
          }
        }
      }
    )

    ElasticTestModel.save({'city': u'Angers'})
    ElasticTestModel.save({'city': u'鴨居'})
    ElasticTestModel.refresh()
    # test the render with default parameters
    result = ElasticTestModel.aggregation_select('city')
    # we get the raw elastic default output
    assert result['hits']
    # check that I have 2 results in the aggregations
    assert len(result['aggregations']['city']['buckets']) == 2
    # same call but diffrent render
    result = ElasticTestModel.aggregation_select('city', select_render=True)
    # check that I have my 2 results in a list format
    assert len(result['city']) == 2

  def test_render_select_aggs(self):
    """Test that it return a formatted select for an aggregation."""
    ElasticTestModel.__index_name__ = '1'
    # set the correct mapping for the city name
    conn = ElasticTestModel.get_connection()
    conn.indices.create(ElasticTestModel.get_index_name())
    conn.indices.put_mapping(
      index=ElasticTestModel.get_index_name(),
      doc_type=ElasticTestModel.__doc_type__,
      body={
        ElasticTestModel.__doc_type__: {
          "properties": {
            "city": {
              "type": "text",
              "fields": {
                "untouched": {
                  "type": "keyword"
                }
              }
            }
          }
        }
      }
    )

    ElasticTestModel.save({'city': u'Angers'})
    ElasticTestModel.save({'city': u'町田'})
    ElasticTestModel.save({'city': u'鴨居'})
    ElasticTestModel.save({'city': u'Mûrs-érigné'})
    ElasticTestModel.refresh()
    result = ElasticTestModel.search(query={'query': {'match_all': {}}, 'aggs': {'city': {'terms': {'field': 'city.untouched'}}}})
    select = ElasticTestModel.render_select_aggs(result, ['city'])
    assert select['city'][0][0] == u'Angers'
    # default we have the count number
    assert select['city'][0][1] == u'Angers (1)'
    select = ElasticTestModel.render_select_aggs(result, ['city'], full_aggs=False)
    # we don't ask for the count
    assert select['city'][0][1] == u'Angers'

  def test_delete_malformatted_dict(self):
    """Test a malformed dict, check that it return an exception and not try to delete the type!!."""
    ElasticTestModel.__index_name__ = '1'
    ElasticTestModel.DEBUG = True
    doc_id = 42
    ElasticTestModel.save({'id': doc_id})
    doc = ElasticTestModel.get_by_id(doc_id)
    assert doc['id'] == doc_id
    # not supported dict!!
    self.assertRaises(NotImplementedError, lambda: ElasticTestModel.delete({'tomato': doc_id}))

  def test_delete_id_int(self):
    """Test the different delete supported syntaxe (int)."""
    # Create a lambda test type to use
    ElasticTestModel.__index_name__ = '1'
    doc_id = 42
    # Add some data
    ElasticTestModel.save({'id': doc_id})
    # check that I have the record
    doc = ElasticTestModel.get_by_id(doc_id)
    assert doc['id'] == doc_id
    # ########### delete by id (int)
    ElasticTestModel.delete(doc_id)
    # check that it deleted
    doc = ElasticTestModel.get_by_id(doc_id)
    assert doc == {}

  def test_delete_id_str(self):
    """Test the different delete supported syntaxe (str)."""
    conn = ElasticTestModel.get_connection()

    ElasticTestModel.__index_name__ = '1'
    str_id = 'camelot'

    # need to force the mapping to str
    conn.indices.create(ElasticTestModel.get_index_name())
    conn.indices.put_mapping(
      index=ElasticTestModel.get_index_name(),
      doc_type=ElasticTestModel.__doc_type__,
      body={
        ElasticTestModel.__doc_type__: {
          "properties": {
            "id": {
              "type": "keyword"
            }
          }
        }
      }
    )
    ElasticTestModel.save({'id': str_id})
    doc = ElasticTestModel.get_by_id(str_id)
    assert doc['id'] == str_id
    ElasticTestModel.delete(str_id)
    # check that it deleted
    doc = ElasticTestModel.get_by_id(str_id)
    assert doc == {}
    # drop the existing index to avoid conflict on mapping
    conn.indices.delete(index=ElasticTestModel.get_index_name())

  def test_not_suported_syntax(self):
    """Test the different delete supported syntaxe."""
    ElasticTestModel.__index_name__ = '1'
    self.assertRaises(NotImplementedError, lambda: ElasticTestModel.delete(ElasticTestModel))

  def test_get_connection(self):
    """Check if the server is here.

    Just a GET request to know if Elastic search is running.

    """
    conn = ElasticTestModel.get_connection()
    assert conn.ping()

  def test_search_on_several_index(self):
    """Test the search on several index."""
    conn = ElasticTestModel.get_connection()
    # Create temp test index with data to search on
    index1 = '1'

    index2 = '2'

    search_word = 'Arthur'
    # Add some data and refresh
    ElasticTestModel.__index_name__ = index1
    ElasticTestModel.save({'namae': search_word})
    ElasticTestModel.refresh()
    # for each index
    ElasticTestModel.__index_name__ = index2
    ElasticTestModel.save({'namae': search_word})
    ElasticTestModel.refresh()

    full_index_1 = '%s%s' % (ElasticTestModel.ELASTIC_INDEX_PREFIX, index1)
    full_index_2 = '%s%s' % (ElasticTestModel.ELASTIC_INDEX_PREFIX, index2)

    result = ElasticTestModel.search(
      {'query': {'term': {'namae': search_word.lower()}}},
      myindex=(full_index_1, full_index_2)
    )
    # check that I have the two results I insert
    assert result['hits']['total'] == 2
    for data in result['hits']['hits']:
      data['_index'] in (index1, index2)

    # delete the index
    conn.indices.delete(index=full_index_1)
    conn.indices.delete(index=full_index_2)

  def test_clean_keyword_end_with_slash(self):
    """Test the clean word ended with slash."""
    conn = ElasticTestModel.get_connection()
    # Create temp test index with data to search on
    ElasticTestModel.__index_name__ = '1'
    search_word = 'Arthur\\'
    # Add some data and refresh don't use name field as it inherit some specific template mapping
    ElasticTestModel.save({'namae': search_word})
    ElasticTestModel.refresh()
    # Here the \ is still here and the query_string return an exception
    from elasticsearch.exceptions import TransportError

    self.assertRaises(TransportError, lambda: ElasticTestModel.search(
      {'query': {'query_string': {'query': search_word, 'fields': ['namae']}}}))
    clean_keyword = ElasticTestModel.clean_keyword(search_word, lower=True)
    # using the cleaned keyword it's ok /!\ need to force the analyzer for this
    # case, cause default one is Kuromoji, defined in the conf file
    query = {
      'query': {'query_string': {'query': clean_keyword, 'fields': ['namae'], 'analyzer': 'whitespace'}}
    }
    result = ElasticTestModel.search(query=query)

    # check that I have the result I inserted
    assert result['hits']['total'] == 1
    # delete the index
    conn.indices.delete(index=ElasticTestModel.get_index_name())

  def test_periodic(self):
    """Test elastic period."""

    ElasticTestPeriod.__index_name__ = None
    generated_index_name = ElasticTestPeriod.get_index_name()

    # save will generate periodic date appended to index
    ElasticTestPeriod.save({'id': 1, 'foo': 'bar', 'foo2': []})

    query = {'query': {'term': {'id': 1}}, 'size': 1}
    ElasticTestPeriod.refresh()
    generated_index_name_on_save = ElasticTestPeriod.get_target_index(query)
    self.assertEqual(generated_index_name, generated_index_name_on_save)

    # not existing document
    query = {'query': {'term': {'id': 5}}, 'size': 1}
    generated_index_name_empty = ElasticTestPeriod.get_target_index(query)
    assert not generated_index_name_empty

  def test_get_by_ids_mget(self):
    """Get the documents by an ids list."""
    # create some dummy document
    ElasticTestModel.__index_name__ = '1'
    ElasticTestModel.save({'id': 1, 'name': 'banana'})
    ElasticTestModel.save({'id': 2, 'name': 'apple'})
    ElasticTestModel.save({'id': 3, 'name': 'carrot'})
    # no need to refresh it make a mget!!
    res = ElasticTestModel.get_by_ids([1, 2, 3])
    self.assertTrue(res)
    # and render_map with total
    self.assertEqual(res['total'], 3)
    self.assertTrue(res[ElasticTestModel.get_index_name()])
    for idx, one_resul in res[ElasticTestModel.get_index_name()].items():
      self.assertIn(one_resul['id'], [1, 2, 3])

  def test_get_by_ids_not_exist(self):
    """Get the documents by an ids list with one that not exist."""
    # create some dummy document
    ElasticTestModel.__index_name__ = '1'
    ElasticTestModel.save({'id': 1, 'name': 'banana'})
    ElasticTestModel.save({'id': 2, 'name': 'apple'})
    ElasticTestModel.save({'id': 3, 'name': 'carrot'})
    # check the with_total option and one docuemnt that not exist
    res = ElasticTestModel.get_by_ids([1, 2, 3, 5], with_total=False)
    # /!\ the mget always return total because we need to compare if we ask document that not exist
    self.assertEqual(res['total'], 4)
    for idx, one_resul in res[ElasticTestModel.get_index_name()].items():
      if idx == '5':
        self.assertFalse(one_resul)

  def test_get_by_ids_sort(self):
    """Get the documents by an ids list and a sort option, use search so need to refresh."""
    # create some dummy document
    ElasticTestModel.__index_name__ = '1'
    ElasticTestModel.save({'id': 1, 'namae': 'banana'})
    ElasticTestModel.save({'id': 2, 'namae': 'apple'})
    ElasticTestModel.save({'id': 3, 'namae': 'carrot'})
    ElasticTestModel.refresh()
    res = ElasticTestModel.get_by_ids([1, 2, 3], sort=[{'namae.keyword': 'desc'}])
    self.assertEqual(res['total'], 3)
    ordered_ids = []
    for idx, one_resul in res[ElasticTestModel.get_index_name()].items():
      ordered_ids.append(idx)
    self.assertEqual(ordered_ids, [3, 1, 2])
    # default order by ids
    self.assertNotEqual(ordered_ids, [1, 2, 3])

  def test_set_alias(self):
    """Test set alias."""
    conn = ElasticTestModel.get_connection()
    index_client = conn.indices

    # create indexes
    # base index class will query the alias index
    class IndexMasterEs(ElasticTestModel):
      __index_name__ = 'index_master'

    mater_index = IndexMasterEs.get_index_name()

    class IndexOneEs(IndexMasterEs):
      __index_name__ = 'index_one'
      ALIASES = [mater_index]

    class IndexTwoEs(IndexMasterEs):
      __index_name__ = 'index_two'
      ALIASES = [mater_index]

    IndexOneEs.save({'id': 1, 'foo': 'bar', 'foo2': []})
    IndexTwoEs.save({'id': 1, 'foo': 'bar', 'foo2': []})

    IndexOneEs.set_alias()
    IndexTwoEs.set_alias()

    alias_group = [IndexOneEs.get_index_name(), IndexTwoEs.get_index_name()]
    exists_alias = index_client.exists_alias(alias_group, mater_index)
    self.assertTrue(exists_alias)

    # clean test index aliases
    index_client.delete_alias(alias_group, mater_index)
    exists_alias = index_client.exists_alias(alias_group, mater_index)
    self.assertFalse(exists_alias)

  def test_get_by_id_periodic(self):
    """Check that we can get the data with get_by_id call in a periodical index."""
    import datetime

    my_first_data = {'id': 1, 'name': 'Banana'}

    ElasticTestPeriod.save(my_first_data, now=None)

    my_older_data = {'id': 2, 'name': 'Potatoes'}
    ElasticTestPeriod.save(my_older_data, now=datetime.datetime(2017, 1, 1))

    # check that I can get my doc by their id
    first_doc = ElasticTestPeriod.get_by_id(my_first_data['id'])
    self.assertEqual(first_doc['name'], my_first_data['name'])

    second_doc = ElasticTestPeriod.get_by_id(my_older_data['id'])
    self.assertEqual(second_doc['name'], my_older_data['name'])

    # check that they were not in the same index
    first_index = ElasticTestPeriod.get_target_index(query={'query': {'term': {'id': my_first_data['id']}}})
    second_index = ElasticTestPeriod.get_target_index(query={'query': {'term': {'id': my_older_data['id']}}})
    self.assertNotEqual(first_index, second_index)

  def test_periodic_search_index_not_yet_exists(self):
    """Test elastic period when the index is not yet exists."""

    ElasticTestPeriod.__index_name__ = None
    generated_index_name = ElasticTestPeriod.get_index_name()

    # test that it will not raise error index not found
    self.assertTrue(ElasticTestPeriod.search({}, myindex=generated_index_name))

  def test_periodic_analyze(self):
    """Check that the keyword search with the analyze call don't raise error when we use a periodic index."""
    from elasticsearch.exceptions import TransportError

    class IndexForAnalyze(ElasticTestModel):
      __index_name__ = '1'

    # Have an existing regular index
    IndexForAnalyze.save({'id': 1, 'namae': 'banana'})

    class IndexPeriodicEs(ElasticTestPeriod):
      """Dummy periodic class."""

    analyzer = 'keyword'
    # in case of periodic index the index don't exist anaylze raise an error
    self.assertRaises(TransportError, lambda: IndexPeriodicEs.analyze('Banana', analyzer))

    class IndexPeriodicEs(ElasticTestPeriod): # noqa
      """Same Dummy class but with the method defined."""

      @classmethod
      def get_analyse_model(cls):
        """To get the analyze index for the analyze part in the keyword search."""
        return IndexForAnalyze

    # in case of periodic index the index don't exist anaylze raise an error
    self.assertTrue(IndexPeriodicEs.analyze('Banana', analyzer))

  def test_alias_index_analyze(self):
    """Check that the the analyze used in keyword search don't raise error for an alias with several index."""
    from elasticsearch.exceptions import TransportError
    analyzer = 'keyword'

    # Have an existing regular index
    ElasticTestModel.__index_name__ = '1'
    ElasticTestModel.save({'id': 1, 'namae': 'banana'})

    # create indexes
    # base index class will query the alias index
    class IndexMasterEs(ElasticTestModel):
      __index_name__ = 'index_master'

    master_index = IndexMasterEs.get_index_name()

    class IndexOneEs(IndexMasterEs):
      __index_name__ = 'index_one'
      ALIASES = [master_index]

    class IndexTwoEs(IndexMasterEs):
      __index_name__ = 'index_two'
      ALIASES = [master_index]

    IndexOneEs.save({'id': 1, 'foo': 'bar', 'foo2': []})
    IndexTwoEs.save({'id': 1, 'foo': 'bar', 'foo2': []})

    IndexOneEs.set_alias()
    IndexTwoEs.set_alias()
    # in case of periodic index the index don't exist anaylze raise an error
    self.assertRaises(TransportError, lambda: IndexMasterEs.analyze('Banana', analyzer))

    class IndexMasterEs(ElasticTestModel):
      __index_name__ = 'index_master'

      @classmethod
      def get_analyse_model(cls):
        """To get the analuze index for the analyze part in the keyword search."""
        return IndexOneEs

    self.assertTrue(IndexMasterEs.analyze('Banana', analyzer))

  def test_is_alias_assigned(self):
    """Check that it return correctly when the alias is assigned."""
    my_first_data = {'id': 1, 'name': 'Banana'}
    my_next_data = {'id': 2, 'name': 'Potatoes'}
    conn = ElasticTestPeriod.get_connection()
    ElasticTestPeriod.save(my_first_data, now=None)
    res = ElasticTestPeriod.is_alias_assigned()
    self.assertFalse(res)
    # push a second doc with an alis set
    ElasticTestPeriod.ALIASES = ['Banana']
    ElasticTestPeriod.save(my_next_data, now=None)
    res = ElasticTestPeriod.is_alias_assigned()
    # the alias is only set on creation if we set the aslias after the first doc it's too late
    self.assertFalse(res)

    # remove the index and create again
    conn.indices.delete(index=ElasticTestPeriod.get_index_name())
    # check that the class still have the ALIASES attribut after deleting
    self.assertEqual(ElasticTestPeriod.ALIASES, ['Banana'])
    ElasticTestPeriod.save(my_first_data, now=None)
    res = ElasticTestPeriod.is_alias_assigned()
    self.assertTrue(res)

  def test_sequence(self):
    """CRUD test for sequence."""
    # out of the box sequence with an index defined
    class SequenceBananaEs(ElasticTestSequence):
      """A sequence to identify my banana with a uniq id."""
      __index_name__ = 'banana'

    seq = SequenceBananaEs.get()
    self.assertEqual(seq, 1)
    # ask again to get the next value
    seq = SequenceBananaEs.get()
    self.assertEqual(seq, 2)

  def test_personal_sequence(self):
    """Overwrite some params."""

    class SequenceBananaEs(ElasticTestSequence):
      """A sequence to identify my banana with a uniq id."""
      __index_name__ = 'banana'

      @classmethod
      def seq_uid(cls, org_uid, raw=None):
        """Set unique sequence per organization in month."""
        import datetime
        month_str = datetime.date.today().strftime('%Y%m')
        seq_uid = '%s-%s' % (org_uid, month_str)
        return seq_uid

    class SequenceTomatoEs(ElasticTestSequence):
      """A sequence to identify tomato."""
      __index_name__ = 'tomato'

      @classmethod
      def seq_uid(cls, org_uid, raw=None):
        """Set unique sequence per organization."""
        return 'tomato_%s' % org_uid

    seq = SequenceBananaEs.get(org_uid='abc')
    self.assertEqual(seq, 1)

    seq = SequenceTomatoEs.get(org_uid='abc')
    self.assertEqual(seq, 1)
    seq = SequenceTomatoEs.get(org_uid='abc')
    seq = SequenceTomatoEs.get(org_uid='abc')
    # for tomato 3rd call
    self.assertEqual(seq, 3)
    seq = SequenceBananaEs.get(org_uid='abc')
    # fo banana 2nd call
    self.assertEqual(seq, 2)
    # Another uid another seq
    seq = SequenceBananaEs.get(org_uid='xyz')
    self.assertEqual(seq, 1)

  def test_sequence_raw(self):
    """Check that the sequence inside is correct."""
    class SequenceBananaEs(ElasticTestSequence):
      """A sequence to identify my banana with a uniq id."""
      __index_name__ = 'banana'

    class SequenceTomatoEs(ElasticTestSequence):
      """A sequence to identify tomato."""
      __index_name__ = 'tomato'

      @classmethod
      def seq_uid(cls, org_uid, raw=None):
        """Set unique sequence per organization."""
        return 'tomato_%s' % org_uid

    seq = SequenceBananaEs.get(raw=True)
    self.assertEqual(seq.get('_id'), SequenceBananaEs.__index_name__) # as we defined nothing it take the index name
    self.assertEqual(seq.get('_version'), 1)
    # Example of sequence for a given uid example by shop
    seq = SequenceTomatoEs.get(raw=True, org_uid='abc')
    self.assertEqual(seq.get('_id'), SequenceTomatoEs.seq_uid(org_uid='abc'))
    self.assertEqual(seq.get('_version'), 1)

  def test_random_sort(self):
    """Check that the random work correctly."""
    import random
    # add 2 doc
    ElasticTestModel.__index_name__ = '1'
    ElasticTestModel.save({'id': 1, 'foo': 'bar'})
    ElasticTestModel.save({'id': 2, 'foo': 'bar2'})
    ElasticTestModel.refresh()

    result_ids = []
    # ask 20 times one document
    for i in range(0, 20):
      raw_search = {
        "function_score": {
          "random_score": {
            "seed": random.randint(10, 55),
            "field": "id"
          }
        }
      }
      result = ElasticTestModel.process_search_query(raw_search=raw_search, sort='random', limit=1, page=1, search_params=None, regular_term_fields=[], regular_terms_fields=[], regular_date_fields=[], post_params=None, aggs=None)
      for idx, one_result in result[ElasticTestModel.get_index_name()].items():
        result_ids.append(idx)
    result_ids = list(set(result_ids))
    # Check that both hit
    self.assertEqual(len(result_ids), 2)
    self.assertIn(1, result_ids)
    self.assertIn(2, result_ids)
