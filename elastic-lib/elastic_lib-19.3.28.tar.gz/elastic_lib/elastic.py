# -*- coding: utf-8 -*-
"""Main file to talk with Elastic server."""
import json
import re
import datetime
from elasticsearch.exceptions import TransportError


class ElasticModel(object):
  """Manage all the actions to ElasticSearch."""

  __index_name__ = None
  __doc_type__ = 'doc'

  ID_KEY = 'id'
  INDEX_PREFIX = None

  ELASTIC_INDEX_PREFIX = ''
  ENV = ''

  DEFAULT_ANALYZER = 'my_analyzer'
  FORCE_ANALYZER = None # force analyser in keyword search for unit tests.
  # display debug in the different request mode 1 in search (i.e. only request)
  DEBUG = False
  DEBUG_QUERY = False # debug only query
  # limit the from size to prevent asking the 10Peta element that not exist
  MAX_FROM_FOR_PAGINATION = 10000001 # 10 mil need to be same as top template
  MODEL_DB = None # for the model that don't have a db model associated, other must overwrite

  KEYWORD_FIELD = 'name' # default field for keyword search if you set nothingn it will search in name field, also used in render select

  # If `true` then refresh the affected shards to make this
  # operation visible to search, if `wait_for` then wait for a refresh
  # to make this operation visible to search, if `false` (the default)
  # then do nothing with refreshes., valid choices are: 'true', 'false',
  # 'wait_for'
  REFRESH_INDEX_OPTION = False
  REFRESH_UPDATE_OPTION = False
  REFRESH_DELETE_OPTION = False

  SKIP_SORT_LIST = ['random'] # list of sort options to ignore

  @classmethod
  def get_index_name(cls):
    """Return class name for a current config."""
    # get index prefix for the application (test_ for test)
    if cls.INDEX_PREFIX:
      prefix = cls.INDEX_PREFIX
    else:
      prefix = cls.ELASTIC_INDEX_PREFIX
    if cls.ENV == 'test':
      prefix += 'test_'
    return prefix + cls.__index_name__

  @classmethod
  def scan(cls, query=None, limit=1000, myindex=None, scroll='5m'):
    """Scan scroll for big pagination when you need to loop throw data bigger than max_result_window (defined in the top template).

    query: dict
    limit: int
    myindex: str or list
    scroll: string

    return {cls.get_index_name(): data(list), total: scroll_size(int), sid: sid(int)}
    """
    from elasticsearch import helpers
    conn = cls.get_connection()

    if not myindex:
      myindex = cls.get_index_name()
    elif isinstance(myindex, (list, tuple)):
      myindex = ','.join(myindex)

    return helpers.scan(
      conn,
      query=query,
      index=myindex,
      size=limit,
      scroll=scroll
    )

  @classmethod
  def get_data(cls, obj):
    """Return object fields in dict format.

    obj: storm object
    """
    data = {}

    # process default fields
    for field in obj.FIELDS_REGULAR:
      value = getattr(obj, field)
      data[field] = value

    # process default array fields. Check content and convert any non-unicode to unicode.
    for field in obj.FIELDS_ARRAY:
      data_list = getattr(obj, field) or []
      if not isinstance(data_list, (list, tuple)):
        raise NotImplementedError # given data is not list.
      new_data_list = []
      for item in data_list:
        new_data_list.append(item)
      data[field] = new_data_list

    # process date fields
    for field in obj.FIELDS_DATE:
      # if date is not set, use now
      value = getattr(obj, field)
      if value:
        # no need to format empty date
        data[field] = value.strftime('%Y-%m-%d %H:%M:%S')

    # process time fields. Saved in extra as string.
    for field in obj.FIELDS_TIME:
      value = getattr(obj, field)
      # save to elastic if only value is set.
      if value:
        data[field] = value.strftime('%H:%M') # '10:00'

    if obj.FIELDS_PICTURE:
      for field in obj.FIELDS_PICTURE:
         # handle picture formating in your model.
        pictures = getattr(obj, field)
        data[field] = pictures

    return data

  @classmethod
  def process_search_query(cls, search_params, regular_term_fields, regular_terms_fields, regular_date_fields, post_params, aggs, sort, page, limit, **kwds):
    """Common function to generate query, send to elastic and return the results dict.

    search_params: dict
    regular_term_fields: dict
    regular_terms_fields: dict
    regular_date_fields: dict
    post_params: dict
    aggs: dict
    sort: dict
    page: int
    limit: int
    kwds: dict (other params)
    - index_name: string
    - highlight: bool
    - id_key: string
    - render: ['raw', 'select', 'query', 'pager'] (default is map)
    - raw_aggs: if set it return the raw aggs
    - no_source: if set it will deactivate _source
    - fields: str or list (Source filtering) don't support dict like _source
    - raw_search: {'any_search'}, will be appended in the [bool][must]
    - page_len: int for the paginator render

      return dict
    """
    # force page as int
    page = int(page)
    if kwds.get('index_name'):
      index_name = kwds.get('index_name')
    else:
      index_name = cls.get_index_name()

    # initialize dict
    if not search_params:
      search_params = {}
    if not post_params:
      post_params = {}

    ret = {
      index_name: {},
      'total': 0,
      'aggs': {}
    }

    filters = cls.process_regular_fields(search_params, regular_term_fields, regular_terms_fields, regular_date_fields)
    query = cls.process_filters(query={}, filters=filters)

    # post params (Aggs not effected)
    post_filter = cls.process_regular_fields(post_params, regular_term_fields, regular_terms_fields, regular_date_fields)

    query, keyword_query = cls.process_keyword_query_filter(query, search_params)

    # append some raw query
    if kwds.get('raw_search'):
      # in some case if we only set a raw_search query is empty
      if not query:
        query = {'bool': {'must': []}}

      query['bool']['must'].append(kwds.get('raw_search'))

    # default
    if not query:
      query = {'match_all': {}}

    my_query = {'query': query}

    # aggregations
    if aggs:
      my_query['aggregations'] = aggs

    # for metadata result only (useful for get ids for deleting)
    if kwds.get('no_source'):
      my_query['_source'] = False
      # for no_srouce option force to raw, cause we'll not have data to format
      kwds['render'] = 'raw'
    # we can't ask for no_source and a list of fields
    elif kwds.get('fields'):
      my_query['_source'] = kwds.get('fields')

    # process post filters
    my_query = cls.process_post_filters(post_filter, my_query)

    # sort (Keep the score sort for keyword search)
    if sort is None:
      if keyword_query: # for keyword default sort by _score
        sort = [{'_score': 'desc'}]
      else:
        # Default
        sort = [{'created_at': 'asc'}, {cls.ID_KEY: 'asc'}]

    # apply sort
    if sort not in cls.SKIP_SORT_LIST:
      my_query['sort'] = sort

    # page start at 0 not 1
    _from = page - 1
    if _from < 0:
      _from = 0

    # pagination
    my_query['from'] = _from * limit
    my_query['size'] = limit

    # append highlight option at the end of the query.
    if kwds.get('highlight'):
      my_query['highlight'] = kwds['highlight']

    # debug query
    if cls.DEBUG_QUERY:
      print ('\n' + '=' * len('= ELASTIC SEARCH QUERY +' * 5) + '\n' + '+ ELASTIC SEARCH QUERY +' * 5 + '\n' + '=' * len('+ ELASTIC SEARCH QUERY =' * 5))
      print ('Class name :', cls.__name__, ' index_name', index_name)
      import json
      print (json.dumps(my_query))

    id_key = kwds.get('id_key') or cls.ID_KEY # default id_key is id.
    if kwds.get('render') == 'query':
      return my_query

    result = cls.search(my_query, myindex=index_name)
    # call the render select, raw...
    if kwds.get('render') == 'select':
      mapped_result = cls.render_select(result)
    elif kwds.get('render') == 'paginator':
      mapped_result = cls.render_paginator(result, page=page, limit=limit, page_len=kwds.get('page_len', 0))
    elif kwds.get('render') == 'raw':
      mapped_result = result
    elif kwds.get('render') == 'pager':
      mapped_result = cls.render_pager(result)
    else:
      mapped_result = cls.render_map(result, id_key=id_key)

    if aggs:
      aggs_result_tmp = result.get('aggregations') or {}
      aggs_result = {}
      if kwds.get('raw_aggs'):
        # return raw aggs
        aggs_result = aggs_result_tmp
      elif aggs_result_tmp:
        from collections import OrderedDict
        aggs_result = {}
        for name in aggs.keys():
          # keep the order of the given aggs.
          if 'buckets' in result['aggregations'][name]:
            aggs_field_ordered_dict = OrderedDict()
            for item in result['aggregations'][name]['buckets']:
              aggs_field_ordered_dict.update({item['key']: item['doc_count']})
            aggs_result[name] = aggs_field_ordered_dict
          elif 'value' in result['aggregations'][name]: # handle the sum, avg aggregations
            aggs_result[name] = result['aggregations'][name]['value']
          else: # this aggregations is not handle please add it here or use aggs_raw=True
            raise NotImplementedError

      ret[index_name] = mapped_result[0]
      ret['total'] = mapped_result[1]
      ret['aggs'] = aggs_result
    else:
      if kwds.get('render') and kwds.get('render') in ('select', 'raw'):
        ret[index_name] = mapped_result
        if kwds.get('render') == 'raw': # fix the total otherwise it always return 0
          ret['total'] = mapped_result['hits']['total']
        elif kwds.get('render') == 'select':
          ret['total'] = len(mapped_result)
      else:
        ret[index_name] = mapped_result[0]
        ret['total'] = mapped_result[1]
    return ret

  @classmethod
  def process_regular_fields(cls, search_params, regular_term_fields, regular_terms_fields, regular_date_fields, index_name=None):
    """Process given params and field dicts and update filters.

    search_params: dict
    filters: dict
    regular_term_fields: dict
    regular_terms_fields: dict
    regular_date_fields: dict
    index_name: string

    return dict (filters)
    """
    # will be used only for debug on local
    all_searched_fields = list(search_params)
    # set default  index name
    if not index_name:
      index_name = cls.get_index_name()

    filters = {
      'must': [],
      'must_not': [],
      'must_or_should': []
    }
    # only regular_term_fields will contain range fields.
    range_fields = {
      'range_lte': 'lte', # Less-than or equal to
      'range_gte': 'gte', # Greater-than or equal to
      'range_lt': 'lt', # Less-than
      'range_gt': 'gt', # Greater-than
    }

    # regular term fields
    for regular_term_field in regular_term_fields:
      # "or" version of the search field.
      or_regular_term_field = 'or_%s' % (regular_term_field)
      # "untouched" version of the search field.
      untouched_regular_term_field = 'untouched_%s' % (regular_term_field)
      # "not" version of the search field.
      not_regular_term_field = 'not_%s' % (regular_term_field)
      # "not_untouched" version of the search field.
      not_untouched_regular_term_field = 'not_untouched_%s' % (regular_term_field)
      # "is_exists" version of the search field.
      is_exists_regular_term_field = 'is_exists_%s' % (regular_term_field)
      # "not_is_exists" version of the search field.
      not_is_exists_regular_term_field = 'not_is_exists_%s' % (regular_term_field)

      # check if field in search params
      if regular_term_field in search_params:
        filters['must'].append({'term': {regular_term_field: search_params[regular_term_field]}})
        if regular_term_field in all_searched_fields:
          all_searched_fields.remove(regular_term_field)

      # check if field has "or" version of the search field.
      if or_regular_term_field in search_params:
        filters['must_or_should'].append({'term': {regular_term_field: search_params[or_regular_term_field]}})
        if or_regular_term_field in all_searched_fields:
          all_searched_fields.remove(or_regular_term_field)

      # check if field has "untouched" version of the search field.
      if untouched_regular_term_field in search_params:
        filters['must'].append({'term': {u'%s.untouched' % (regular_term_field): search_params[untouched_regular_term_field]}})
        if untouched_regular_term_field in all_searched_fields:
          all_searched_fields.remove(untouched_regular_term_field)

      # check if not field in search params
      if not_regular_term_field in search_params:
        filters['must_not'].append({'term': {regular_term_field: search_params[not_regular_term_field]}})
        if not_regular_term_field in all_searched_fields:
          all_searched_fields.remove(not_regular_term_field)

      # check if not untouched field in search params
      if not_untouched_regular_term_field in search_params:
        filters['must_not'].append({'term': {u'%s.untouched' % (regular_term_field): search_params[not_untouched_regular_term_field]}})
        if not_untouched_regular_term_field in all_searched_fields:
          all_searched_fields.remove(not_untouched_regular_term_field)

      # check if is_exists field in search params
      if is_exists_regular_term_field in search_params:
        filters['must'].append({'constant_score': {'filter': {'exists': {'field': regular_term_field}}}})
        if is_exists_regular_term_field in all_searched_fields:
          all_searched_fields.remove(is_exists_regular_term_field)

      # check if not_is_exists field in search params
      if not_is_exists_regular_term_field in search_params:
        filters['must_not'].append({'constant_score': {'filter': {'exists': {'field': regular_term_field}}}})
        if not_is_exists_regular_term_field in all_searched_fields:
          all_searched_fields.remove(not_is_exists_regular_term_field)

      # loop through all range fields and check if search params.
      for range_field, range_type in range_fields.items():
        # generate field name
        _field = '%s_%s' % (range_field, regular_term_field)
        # alias
        elastic_field = regular_term_field
        # check if given search params have the range field.
        if _field in search_params:
          # get value
          value = search_params[_field]
          # append generated range query.
          filters['must'].append({"range": {elastic_field: {range_type: value}}})
          all_searched_fields.remove(_field)

    # regular terms fields
    for regular_terms_field, elastic_field in regular_terms_fields:
      # "or" version of the search field.
      or_regular_terms_field = 'or_%s' % (regular_terms_field)

      # "untouched" version of the search field.
      untouched_regular_terms_field = 'untouched_%s' % (regular_terms_field)

      # "not" version of the search field.
      not_regular_terms_field = 'not_%s' % (regular_terms_field)

      # "not" untouched version of the search field.
      not_untouched_regular_terms_field = 'not_untouched_%s' % (regular_terms_field)

      # check if alternative field name is provided
      if not elastic_field:
        # use default field name.
        elastic_field = regular_terms_field

      # check if field in search params
      if regular_terms_field in search_params:
        filters['must'].append({'terms': {elastic_field: search_params[regular_terms_field]}})
        if regular_terms_field in all_searched_fields:
          all_searched_fields.remove(regular_terms_field)

      # check if field has "or" version of the search field.
      if or_regular_terms_field in search_params:
        filters['must_or_should'].append({'terms': {elastic_field: search_params[or_regular_terms_field]}})
        if or_regular_terms_field in all_searched_fields:
          all_searched_fields.remove(or_regular_terms_field)

      # check if field has "untouched" version of the search field.
      if untouched_regular_terms_field in search_params:
        filters['must'].append({'terms': {u'%s.untouched' % (elastic_field): search_params[untouched_regular_terms_field]}})
        if untouched_regular_terms_field in all_searched_fields:
          all_searched_fields.remove(untouched_regular_terms_field)

      # check if not field in search params
      if not_regular_terms_field in search_params:
        filters['must_not'].append({'terms': {elastic_field: search_params[not_regular_terms_field]}})
        if not_regular_terms_field in all_searched_fields:
          all_searched_fields.remove(not_regular_terms_field)

      # check if not untouched field in search params
      if not_untouched_regular_terms_field in search_params:
        filters['must_not'].append({'terms': {u'%s.untouched' % (elastic_field): search_params[not_untouched_regular_terms_field]}})
        if not_untouched_regular_terms_field in all_searched_fields:
          all_searched_fields.remove(not_untouched_regular_terms_field)

    # regular date fields
    for regular_date_field, elastic_field, date_param in regular_date_fields:
      if regular_date_field in search_params:
        value = search_params[regular_date_field]
        if isinstance(value, datetime.datetime):
          value = value.strftime("%Y-%m-%d %H:%M:%S")
        elif not isinstance(value, str):
          raise NotImplementedError
        filters['must'].append({"range": {elastic_field: {date_param: value}}})
        all_searched_fields.remove(regular_date_field)

    # special field last clean before check
    if u'keyword' in all_searched_fields:
      all_searched_fields.remove(u'keyword')
    # if you try to filter on a field that is not defined in term, terms or date or you made a typo

    if all_searched_fields:
      print ('&' * 42)
      print ('Check that you defined the following fields in your search_model or you did not misspell.')
      print ('ModelEs: %s Index: %s' % (cls.__name__, cls.get_index_name()))
      print ('Not handled fields : ', all_searched_fields)
      print ('&' * 42)
      raise NotImplementedError

    return filters

  @classmethod
  def process_filters(cls, query, filters):
    """Process filters and update the query.

    query: dict
    filters: dict

    return dict.
    """
    # Process filters
    # if filters['must'] or filters['must_not']:
    #   query = {'bool': {'filter': {'bool': {}}}}
    #   if filters['must']:
    #     query['bool']['filter']['bool']['must'] = filters['must']
    #   if filters['must_not']:
    #     query['bool']['filter']['bool']['must_not'] = filters['must_not']

    # Process filters
    if filters.get('must') or filters.get('must_not') or filters.get('must_or_should'):
      query = {'bool': {}}
      # must
      if filters.get('must'):
        query['bool']['must'] = [{'bool': {'must': filters['must']}}]
      # must not
      if filters.get('must_not'):
        if not query['bool'].get('must'):
           query['bool']['must'] = []
        query['bool']['must'].append({'bool': {'must_not': filters['must_not']}})
      # should
      if filters.get('must_or_should'):
        # wraps all must fields under should and append to top level must.
        if not query['bool'].get('must'):
           query['bool']['must'] = []
        query['bool']['must'].append({'bool': {'should': filters['must_or_should']}})

    return query

  @classmethod
  def process_keyword_query_filter(cls, query, search_params):
    """Update query dict for given keyword.

    query: dict
    search_params: dict

    return tuple (query dict, keyword_query)
    """

    # keyword query
    keyword_query = None
    if search_params.get('keyword'):
      # TODO: Update process keyword after mapping complete.
      keyword_query = cls._process_keyword(search_params.get('keyword'))

    # Add keyword query to filtered query. (To avoid: No filter registered for [query_string])
    if keyword_query:
      # check filtered key exist
      if not query.get('bool'):
        query['bool'] = {'must': []}

      # check query key exist
      if not query['bool'].get('must'):
        query['bool']['must'] = []

      # check if keyword query use must or should
      must_or_should = 'must' if 'must' in keyword_query['bool'] else 'should'

      # Extend keyword query bool values to query
      query['bool']['must'].append({'bool': {must_or_should: keyword_query['bool'][must_or_should]}})
    return query, keyword_query

  @classmethod
  def process_post_filters(cls, post_filter, my_query):
    """Process post filters dict and update my_query.

    post_filter: dict
    my_query: dict
    return dict (my_query)
    """
    # post filters
    if post_filter['must'] or post_filter['must_not']:
      my_query['post_filter'] = {'bool': {}}
      if post_filter['must']:
        my_query['post_filter']['bool']['must'] = post_filter['must']
      if post_filter['must_not']:
        my_query['post_filter']['bool']['must_not'] = post_filter['must_not']
    return my_query

  @classmethod
  def _process_keyword(cls, keyword):
    """Basic keyword search assume that the model have a name and tags fields to work out of the box for simple model."""
    keyword_cleaned = cls.clean_keyword(keyword)
    keyword_low = keyword_cleaned.replace("-", " ").strip()

    analyzer = cls.DEFAULT_ANALYZER

    if keyword_cleaned:
      analyzer = cls.get_analyzer(keyword_cleaned)

    return {
      'bool': {
        'should': [
          {
            'query_string': {
              'query': '%s*' % keyword_low,
              'fields': [
                'name^5',
                'name.*^5',
                'tags^2',
              ],
              'default_operator': 'AND',
              'analyzer': analyzer,
              'fuzziness': 'auto'
            }
          },
          {
            'term': {
              'name.untouched': keyword
            }
          },
          {
            'term': {
              'tags.untouched': keyword
            }
          }
        ]
      }
    }

  @classmethod
  def search_shards(cls, id):
    """Return the number of the primary shard where the document is.

    id: int
    """
    conn = cls.get_connection()
    result = conn.search_shards(index=cls.get_index_name(), routing=id)
    # I must have 1 result on first level
    if len(result['shards']) == 1:
      # I can have several value depends on the server configurtion, if there's replicas or not
      for one_shard in result['shards'][0]:
        if one_shard.get('primary') is True:
          return one_shard.get('shard')
    return None

  @classmethod
  def exists(cls, id):
    """Return true or false if the document exist or not.

    id: int id to check

    return bool

    """
    conn = cls.get_connection()
    return conn.exists(index=cls.get_index_name(), doc_type=ElasticModel.__doc_type__, id=id)

  @classmethod
  def get_settings(cls, field):
    """Get the settings of the current index."""
    conn = cls.get_connection()
    result = conn.indices.get_settings(index=cls.get_index_name())
    index_name = result.keys()[0]
    return result[index_name]['settings']['index'].get(field, None)

  @classmethod
  def put_settings(cls, my_data):
    """Merge/Set the given settings.

    ex:
    # to update the max result window
    put_settings({'max_result_window': 100000})
    # to add an analyzer
    put_settings({
      "analysis": {
        "analyzer": {
          "no_punctuation_analyzer": {
            "tokenizer": "kuromoji_no_punctuation_dict",
            "filter": ["kuromoji_st", "kuromoji_syn", "cjk_width"]
          }
        },
        "tokenizer": {
          "kuromoji_no_punctuation_dict": {
             "type": "kuromoji_tokenizer",
             "mode": "search",
             "discard_punctuation": "true",
             "user_dictionary": "luxeysdict_ja.txt"
          }
        }
      }
    })
    """
    conn = cls.get_connection()
    return conn.indices.put_settings(body=my_data, index=cls.get_index_name())

  @classmethod
  def validate_query(cls, query):
    """Check the syntax, mainly for unit test when we dynamicaly build query."""
    conn = cls.get_connection()
    # params must be empty dict can't be None or the lib will raise error (elastcsearch-python lib > 5.x)
    return conn.indices.validate_query(index=cls.get_index_name(), body=query, params={})

  @classmethod
  def get_connection(cls):
    """Create the connection to ElasticSearch."""
    # you need to overwrite this one to create your own connection
    return False

  @classmethod
  def save(cls, my_data, params=None, render=None):
    """Make the job. Create if not exist else update.

    my_data: dict or storm object
    params: more params ex: used for parent/child relations
    render: str

    """
    if not isinstance(my_data, dict):
      my_data = cls.get_data(my_data)

    # check json data
    json.dumps(my_data)

    if not params:
      params = {}

    conn = cls.get_connection()
    res = conn.index(
        index=cls.get_index_name(),
        doc_type=ElasticModel.__doc_type__,
        id=my_data.get("id") or '',
        params=params,
        body=my_data,
        refresh=cls.REFRESH_INDEX_OPTION,
    )
    if render == 'raw':
      return res
    return cls.get_by_id(res.get('_id'))

  @classmethod
  def update(cls, my_id, my_data):
    """Update partial documents."""
    conn = cls.get_connection()
    if not my_data.get('doc'):
      my_data = {'doc': my_data}

    return conn.update(
        index=cls.get_index_name(),
        doc_type=ElasticModel.__doc_type__,
        id=my_id,
        body=my_data,
        refresh=cls.REFRESH_UPDATE_OPTION,
    )

  @classmethod
  def delete(cls, data):
    """Support Delete by a string id or int id.

    data: string or int

    data = 1 if you want to delete the document 1 (int id)
    data = 'tag1' if you want to delete the document 'tag1' (string id)
    """
    conn = cls.get_connection()
    params = {}
    if(isinstance(data, (int, str))):
      params['id'] = data
    else:
      raise NotImplementedError

    if params.get('id'):
      try:
        conn.delete(index=cls.get_index_name(), doc_type=ElasticModel.__doc_type__, id=params.get('id'), refresh=cls.REFRESH_DELETE_OPTION)
      except TransportError:
        # if the document don't exist do nothing
        pass

  @classmethod
  def delete_by_query(cls, query):
    """Delete data by query."""
    conn = cls.get_connection()
    return conn.delete_by_query(index=cls.get_index_name(), body=query, doc_type=ElasticModel.__doc_type__)

  @classmethod
  def cascade(cls, id, parent_id=None):
    """Delete the current object and the relative define in cascade.

    id: int
    parent_id: int for parent child relations

    """
    # build the query to delete the relative objects
    if cls.relations:
      for relation in cls.relations:
        if relation.get("model") and relation.get("relation_key"):
          # build the model class
          model_elastic = relation.get("model")
          mod_elastic = __import__("model", fromlist=model_elastic)
          type_es = getattr(mod_elastic, model_elastic)# noqa build model instance from string
          type_es.delete({"query": {"term": {relation.get("relation_key"): id}}})

    # then delete the main object
    if parent_id:
      cls.delete(id, parent_id)
    else:
      cls.delete(id)

  @classmethod
  def refresh(cls):
    """Force the refresh of the index when you insert, delete or update and search after."""
    cls._refresh(cls.get_index_name())

  @classmethod
  def _refresh(cls, index_name):
    """Force the refresh of the index when you insert, delete or update and search after."""
    conn = cls.get_connection()
    conn.indices.refresh(index=index_name)

  @classmethod
  def analyze(cls, data, analyzer, return_as_tokens=False):
    """Make an analyze request.

    data: string to be analyzed.
    analyzer: str name of the analyzer we'll use.
    return_as_tokens: bool, flags for return type list or string.

    return: ElasticSearch result if return_as_tokens not set, else return list.

    """
    conn = cls.get_connection()
    # force data to become a dict if it's just a string, plain text is deprected
    # plain text bodies is deprecated and this feature will be removed in the next major release. Please use the text param in JSON
    if isinstance(data, str):
      data = {'text': data}
    # pass the analyzer in body cause pass as params is deprecated from 5.1:
    # analyzer request parameter is deprecated and will be removed in the next major release. Please use the JSON in the request body instead request param
    data['analyzer'] = analyzer

    analyze_model = cls.get_analyse_model()
    if analyze_model:
      index_name = analyze_model.get_index_name()
    else:
      index_name = cls.get_index_name()

    result = conn.indices.analyze(index=index_name, body=data)
    value = []
    # in case of error elastic don't return the "tokens" key
    for token in result.get("tokens", []):
      value.append(token["token"])

    if return_as_tokens:
      # Return list of tokens.
      return value
    return ' '.join(value)

  @classmethod
  def search(cls, query, pager=False, myindex=None, params=None):
    """Perform the search.

    for _suggest suffix check the doc to set the right mapping and index
    http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-suggesters-completion.html

    query: dict
    pager: bool, wrap the data in a list more easy to fetch for pagination
    myindex: str or list
    params: str

    return: ElasticSearch result.

    """
    from elasticsearch.exceptions import NotFoundError
    conn = cls.get_connection()
    result = {}
    if not myindex:
      myindex = cls.get_index_name()

    if isinstance(myindex, (list, tuple)):
      myindex = ','.join(myindex)

    kwds = {'index': myindex, 'body': query}
    if myindex:
      kwds['index'] = myindex
    if params:
      kwds['params'] = params

    if isinstance(query, dict) and query.get('from') and query.get('from') > cls.MAX_FROM_FOR_PAGINATION:
      # set the max in the query
      query['from'] = cls.MAX_FROM_FOR_PAGINATION
      kwds['body'] = query

    # just display the name of the missing index for debugging
    # run this to set the missing index: python converter.py init_elastic_schema
    try:
      result = conn.search(index=kwds['index'], body=kwds['body'])
    except NotFoundError as e:
      print ('*' * 102)
      print ('')
      print (' ' * 33, 'Not found index: ', kwds['index'])
      print ('')
      print ('*' * 102)
      raise e

    if pager:
      return cls.render_pager(result)

    return result

  @classmethod
  def send(cls, bulk):
    """Send a bulk.

    bulk: dict

    return: ElasticSearch result.

    """
    conn = cls.get_connection()
    return conn.bulk(body=bulk)

  @classmethod
  def pager(cls, query=None, page=1, size=20, sort=None):
    """Get records on the selected page.

    query dict
    page: int
    size: int
    sort: dict

    return: records, total

    """
    # force a match all query by default
    if not query:
      query = {"query": {"match_all": {}}}

    # build the query
    my_query = query

    if sort:
      my_query["sort"] = sort

    # pagination
    my_query["from"] = (page - 1) * size
    my_query["size"] = size

    return cls.search(query=my_query, pager=True)

  @classmethod
  def count(cls, query=None, myindex=None):
    """Get the total of records. Return the count only.

    query: dict to request on specific result
    myindex: str example: pictures,albums <--- no space between the values

    return: number of result

    """
    conn = cls.get_connection()

    if query:
      # force the size to 0
      query['size'] = 0
    else:
      # no query provided just get all
      query = {'query': {'match_all': {}}, 'size': 0}

    if not myindex:
      myindex = cls.get_index_name()
    result = conn.search(index=myindex, body=query)

    return result['hits']['total']

  @classmethod
  def update_by_query(cls, body, scroll_size=1000, params=None, myindex=None):
    """Update records by query.

    body: dict (query)
    scroll_size: int, By default _update_by_query uses scroll batches of 1000. You can change the batch size with the scroll_size.
    params: more params

    return response (dict)
    """
    # elastic expect dict (not None)
    if not params:
      params = {}
    # check json query and script
    json.dumps(body)

    if not myindex:
      myindex = cls.get_index_name()

    conn = cls.get_connection()
    result = conn.update_by_query(
      index=myindex,
      params=params,
      body=body,
      scroll_size=scroll_size
    )
    return result

  @classmethod
  def bulk_data(cls, data, action="index"):
    """Build a bulk from data.

    data: dict
    action: any of [create, update, index, delete]

    return: formatted data for bulk in Json.

    """
    bulk_header = {
      action: {
        "_index": cls.get_index_name(),
        "_type": ElasticModel.__doc_type__
      }
    }

    # if it's not a dict it's the db object so we need to get the formatted data first
    if not isinstance(data, dict):
      data = cls.get_data(data)

    # ignore invalid data.
    if not data:
      return ''

    # for some data I don't have id
    if data.get("id"):
      bulk_header[action]["_id"] = data["id"]

    if action == "update":
      data = {"doc": data}

    # for delete
    if action == "delete":
       return json.dumps(bulk_header) + '\n'

    return json.dumps(bulk_header) + '\n' + json.dumps(data) + '\n'

  @classmethod
  def mget(cls, data):
    """Make a multi get

    data: list

    list: [1, 2, 3] <-- get the document 1,2,3 for the current class

    Check the doc for the different supported options
    https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-multi-get.html

    """
    from elasticsearch.exceptions import TransportError
    from collections import OrderedDict
    # transform the result get only the source
    formatted_result = OrderedDict()

    conn = cls.get_connection()
    try:
      # don't cast the id here id can be string or int
      result = conn.mget(index=cls.get_index_name(), body={'ids': data})
    except TransportError:
      return {'total': 0, cls.get_index_name(): formatted_result}

    for one_doc in result.get('docs'):
      # add the content only for the found one
      if one_doc.get('_source'):
        if cls.ID_KEY == '_id':
          formatted_result.update({one_doc[cls.ID_KEY]: one_doc['_source']})
        else:
          formatted_result.update({one_doc['_source'][cls.ID_KEY]: one_doc['_source']})
      else:
        formatted_result.update({one_doc.get('_id'): False})

    return {'total': len(formatted_result), cls.get_index_name(): formatted_result}

  @classmethod
  def msearch(cls, body, keys, header=None):
    """Make a multi search.

    body: list of dict query
    keys: list of key I need to set to put the data behind

    """
    conn = cls.get_connection()
    new_body = []
    index_name = None

    # you must provide a key for each request
    assert len(body) == len(keys)

    if not header:
      index_name = cls.get_index_name()
    else:
      # you must provide one header for each body
      assert len(header) == len(body)
      # some case we use the generic Elastic model so index_name is not set so we take from the header
      if not index_name:
        # header
        index_name = header[0]['index_name']

    # set the header
    for idx, row in enumerate(body):
      if header and header[idx]:
        new_header = {'index': header[idx].get('index_name')}
        new_body.append(new_header)
      else:
        new_body.append({})

      new_body.append(row)

    result = conn.msearch(index=index_name, body=new_body)

    # transform the result to standard format
    standard_result = {}

    for idx, one_response in enumerate(result['responses']):
      # set the result by key
      one_key = keys[idx]
      idx_name = index_name
      if header and header[idx]:
        idx_name = header[idx].get('index_name')
      mapped_result, total = cls.render_map(one_response, mindex=True)
      if one_response.get('aggregations'):
        mapped_result['aggs'] = one_response.get('aggregations')

      standard_result.update({one_key: {'total': total, idx_name: mapped_result}})
    return standard_result

  @classmethod
  def get_by_id(cls, id, raw=False):
    """Get the document by his Id.

    id: int
    raw: bool if True keep the metadata

    return: ElasticSearch result or json dict

    """
    params = {}
    conn = cls.get_connection()

    try:
      # don't cast the id here id can be string or int
      result = conn.get(index=cls.get_index_name(), doc_type=ElasticModel.__doc_type__, id=id, params=params)
    except TransportError:
      # return empty dict if not found
      result = {}

    if not raw and result:
      result = result['_source']
      # if there's no id field inject it
      if not result.get('id'):
        result['id'] = id

    return result

  @classmethod
  def get_by_ids(cls, ids, with_total=True, sort=None):
    """Get the documents by their ids render an id dict.

    ids: [int]
    with_total: bool
    sort: [list]

    return: dict

    """
    if sort:
      query = {'query': {'ids': {'values': ids}}, 'size': len(ids)}
      query['sort'] = sort
      result = cls.search(query=query)
      formatted_result, total = cls.render_map(result, with_total=with_total)
      return {'total': total, cls.get_index_name(): formatted_result}
    else:
      return cls.mget(ids)

  @classmethod
  def render_paginator(cls, result, page=1, limit=10, page_len=0):
    """Format a raw ElasticSearch result in paginator object format."""
    from .utils import ElasticSearchPaginatorResult
    e = ElasticSearchPaginatorResult(result)

    return cls._render_paginator(e, page, limit, page_len)

  @classmethod
  def render_paginator_for_es_result(cls, records, total, page=1, limit=10, page_len=0, reverse=False):
    """DEPRECATED WILL BE REMOVED DO NOT USE.

    Format an orderedDict ElasticSearch result in paginator object format.

    records: ordered dict (elastic result)
    """
    from .utils import ElasticSearchPaginatorDict
    e = ElasticSearchPaginatorDict(records, total, reverse)

    return cls._render_paginator(e, page, limit, page_len)

  @classmethod
  def _render_paginator(cls, e, page, limit, page_len):
    """Commmon code to render a paginator."""
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

    paginator = Paginator(e, limit)

    if not page_len:
      page_len = 3
    try:
      paginated_data = paginator.page(page)
    except PageNotAnInteger:
      paginated_data = paginator.page(1)
    except EmptyPage:
      paginated_data = paginator.page(paginator.num_pages)

    # Get the index of the current page
    index = paginated_data.number - 1  # edited to something easier without index
    # This value is maximum index of your pages, so the last page - 1
    max_index = len(paginator.page_range)
    # You want a range of 7, so lets calculate where to slice the list
    start_index = index - page_len if index >= page_len else 0
    end_index = index + page_len if index <= max_index - page_len else max_index
    # Get our new page range. In the latest versions of Django page_range returns
    # an iterator. Thus pass it to list, to make our slice possible again.
    page_range = list(paginator.page_range)[start_index:end_index]

    total = paginated_data.paginator.count
    int_page = paginated_data.number
    item_start = (int_page - 1) * limit + 1
    item_end = total if item_start + limit > total else item_start + limit - 1

    pages_data = {
      'page_range': page_range,
      'total': total,
      'item_start': item_start,
      'item_end': item_end
    }

    result = paginated_data, pages_data

    return result, total # total is included 2 times one in pages_data and here for compatibility with other format

  @classmethod
  def render_map(cls, result, with_total=True, hydrate=None, id_key='id', mindex=False):
    """Format an ElasticSearch result in map format, dict with id key, and dict object as value.

    /!\ if result is malformed it's not my business I only render so I'll return an empty result

    result: ElasticSearch result
    with_total: bool
    hydrate: dict
    id_key: string
    mindex: bool True if we make a search on several indices, to have unique id

    return: formatted dict, total or only dict

    """
    # use an ordered dict to keep the same order than the request
    from collections import OrderedDict
    result_map = OrderedDict()
    total = 0
    # handle case where the status is 404 or 500 to prevent returning error from code that hard to debug and not relared with rendering data
    # we expect that from here we receive result that we are sure that index exist and there's no error in the request
    # in other case we return empty result, check your result before asking for a render, it's not my job to check the data I only render
    if result.get('hits') and result["hits"]["total"] > 0:
      total = result["hits"]["total"]
      for raw_result in result["hits"]["hits"]:
        es_result = raw_result["_source"]

        # use ID_KEY for model having that different than 'id'
        if mindex:
          key_id = '%s_%s' % (raw_result['_index'], raw_result['_id'])
        elif hasattr(cls, 'ID_KEY') and cls.ID_KEY == '_id':
          id_key = cls.ID_KEY
          key_id = raw_result[id_key]
          es_result['id'] = raw_result["_id"]
        else:
          key_id = es_result[id_key]

        if raw_result.get('highlight'):
          es_result.update({'highlight': raw_result['highlight']})
        if hydrate:
          if not isinstance(hydrate, list):
            hydrates = [hydrate]
          else:
            hydrates = hydrate
          for one_hydrate in hydrates:
            if one_hydrate.get("field"):
              if es_result.get(one_hydrate.get("aggs_field")):
                # multi values
                es_result[one_hydrate["field"]] = one_hydrate["data"].get(es_result[one_hydrate["aggs_field"]])
              elif one_hydrate.get("data"):
                es_result[one_hydrate["field"]] = one_hydrate["data"]
        result_map[key_id] = es_result

    if with_total:
      return result_map, total

    return result_map

  @classmethod
  def render_select(cls, result, fields=''):
    """Format the result to feed a select with id and name field.

    result: dict
    fields: list

    return: list with id and name

    """
    if not fields:
      fields = (cls.ID_KEY, cls.KEYWORD_FIELD)

    formatted_result = []

    for p in result["hits"]["hits"]:
      if fields[0] == '_id':
        first_field = p[fields[0]]
      else:
        first_field = p["_source"][fields[0]]

      formatted_result.append((first_field, p["_source"][fields[1]]))

    return formatted_result

  @classmethod
  def aggregation_select(cls, fields, size=50, select_render=False, full_aggs=True, query=None, only_count=False):
    r"""Get the aggregations for select box.

    use case : aggregation_select("last_name", select_render=True, full_aggs=True)
    return {"last_name": [(u"toto", u"toto (3)"), (u"tata", u"tata (2)"), (u"titi", u"titi (1)")...]}

    you can also pass a list of fields aggregation_select(("last_name", "first_name"))
    check the unit test for more use case!

    fields: list
    size: int
    select: bool (formatted to enter in a select)
    full_aggs: bool (return the doc count or not for the select_render) ex: TRUE --> Tokyo (10) FALSE ---> Tokyo
    query: dict
    only_count: bool if we want only the count example return {"last_name": [(u"toto", u"3"), (u"tata", u"2")...]}

    /!\ replace the . in the name by _ aggs only support name with _ and -

    return: ElasticSearch result

    """
    if not fields:
      return {}

    my_query = {}

    if not isinstance(fields, (list, tuple)):
      fields = [fields]

    if query:
      # accept query with query key or not
      if query.get("query"):
        query = query.get("query")
      my_query["query"] = query
    my_query["aggregations"] = cls.build_aggregation(fields, size)
    # we only need aggregations don't need hits
    my_query["size"] = 0
    result = cls.search(my_query, params="search_type=count")

    if select_render:
      return cls.render_select_aggs(result, fields, full_aggs, only_count=only_count)

    return result

  @classmethod
  def render_select_aggs(cls, result, fields, full_aggs=True, only_count=False):
    """Render the aggregation result in a list.

    result: ElasticSearch result w/aggregations key
    fields: list
    full_aggs: bool

    return: result

    """
    if isinstance(fields, (list, tuple)):
      result_map = {}
      for field in fields:
        field_name = field.replace(".", "_")
        # manage filtered aggs
        if result["aggregations"].get("%s_filtered" % field_name):
          aggreg_list = result["aggregations"]["%s_filtered" % field_name][field_name]
        else:
          aggreg_list = result["aggregations"][field_name]

        if only_count:
          result_map[field] = [(p["key"], "%s" % (p["doc_count"])) for p in aggreg_list["buckets"]]
        elif full_aggs:
          result_map[field] = [(p["key"], "%s (%s)" % (p["key"], p["doc_count"])) for p in aggreg_list["buckets"]]
        else:
          result_map[field] = [(p["key"], "%s" % (p["key"])) for p in aggreg_list["buckets"]]

      return result_map
    else:
      field_name = fields[0].replace(".", "_")
      if only_count:
        result = [(p["key"], "%s" % (p["doc_count"])) for p in result["aggregations"][field_name]["buckets"]]
      elif full_aggs:
        result = [(p["key"], "%s (%s)" % (p["key"], p["doc_count"])) for p in result["aggregations"][field_name]["buckets"]]
      else:
        result = [(p["key"], "%s" % p["key"]) for p in result["aggregations"][field_name]["buckets"]]

    return result

  @classmethod
  def render_pager(cls, result):
    """Render a result in pager mode.

    result: raw elastic result

    """
    records = []
    total = result["hits"]["total"]
    if total:
      for r in result["hits"]["hits"]:
        record = r["_source"]
        record["id"] = r["_id"]
        records.append(record)
    return records, total

  @classmethod
  def build_aggregation(cls, fields, size, filters=None):
    r"""Build the aggregation for a field or a list of fields.

      /!\ The fields MUST be multifield with an untouched sub-field

    field: list or str
    size: int
    filters: list

    return: aggs

    """
    aggs_list = {}
    aggs = {}

    # put the string a list to manage it in the loop under
    if isinstance(fields, str):
      fields = (fields, )

    for field in fields:
      if isinstance(field, (tuple, list)):
        nested_aggs = []
        for idx, sub_field in enumerate(field):
          if idx == 0:
            continue
          nested_aggs.append({"aggregations": {sub_field: {"terms": {"field": "%s.untouched" % sub_field}}}})
        agg = {field[0]: {"field": "%s.untouched" % field[0], "size": size, "nested_aggs": nested_aggs}}
      else:
        agg = {field: {"field": "%s.untouched" % field, "size": size}}

      if aggs_list:
        aggs_list.update(agg)
      else:
        aggs_list = agg

    for key, agg in aggs_list.items():
      # aggregations name can't contain "."
      aggs_name = key.replace(".", "_")
      aggregation = {
        "terms": {
          "field": agg["field"],
          "size": agg["size"],
          "order": {"_count": "desc"}
        }
      }

      # add the filters
      if filters:
        aggs["%s_filtered" % aggs_name] = {"filter": filters}
        aggs["%s_filtered" % aggs_name]["aggregations"] = {aggs_name: aggregation}
      else:
        aggs[aggs_name] = aggregation
      if agg.get("nested_aggs"):
        aggs[aggs_name] = {"terms": aggs[aggs_name]["terms"], "aggregations": agg["nested_aggs"][0]["aggregations"]}

    return aggs

  @classmethod
  def index_op(cls, action, index=None):
    """Perform open close operations on the current index.

    action: str ["open", "close", "restart"]
    index: str (optional)

    """
    result = False

    if not index:
      index = cls.get_index_name()
    if action in ('open', 'close', 'restart'):
      conn = cls.get_connection()
      index_client = conn.indices

      if action == 'restart':
        result = index_client.close(index=index)
        result = index_client.open(index=index)
      elif action == 'open':
        result = index_client.open(index=index)
      elif action == 'close':
        result = index_client.close(index=index)
    return result

  @classmethod
  def get_alias(cls, index_name=None):
    """Get the index alias as list."""
    conn = cls.get_connection()
    if not index_name:
      index_name = cls.get_index_name()
    alias_list = conn.indices.get_alias(index_name)

    return list(alias_list[cls.get_index_name()]['aliases'].keys())

  @classmethod
  def set_alias(cls, index_name=None):
    """Set index alias from alias group constant."""
    # just do nothing if the index is not concerned or alias already set
    if not index_name and not hasattr(cls, 'ALIASES') or (hasattr(cls, 'ALIASES') and cls.is_alias_assigned()):
      return False

    if not index_name:
      index_name = cls.get_index_name()

    conn = cls.get_connection()
    for one_alias in cls.ALIASES:
      result = conn.indices.put_alias(index_name, one_alias)
    return result

  @classmethod
  def get_aliased(cls, alias):
    """Get the indices for which the alias is set."""
    booking_es = cls.get_connection()
    result = booking_es.indices.get_alias(alias)
    return list(result.keys())

  @classmethod
  def is_alias_assigned(cls):
    """Check whether the alias is set or not."""
    conn = cls.get_connection()
    if not hasattr(cls, 'ALIASES'):
      return False
    return conn.indices.exists_alias(cls.get_index_name(), cls.ALIASES)

  @classmethod
  def remote_reindex_wsa(cls, script=None, source_query=None, params=None, target_index=None, pipeline=None):
    """Remote reindex With Switch Alias."""
    import datetime
    from elasticsearch.exceptions import NotFoundError
    # generate uniq index name
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M')
    alias = cls.get_index_name()
    target_index = '%s_%s' % (alias, timestamp)
    conn = cls.get_connection()

    # create the index
    conn.indices.create(target_index)
    # by default we wait for completition as index are suppose to be small and not timeout
    # if the server is down it will timeout and raise error
    if not params:
      params = {'wait_for_completion': 'true'}

    cls.remote_reindex(script=script, source_query=source_query, params=params, target_index=target_index, pipeline=pipeline)

    index_to_delete = None

    cls._refresh(target_index) # force refresh before make the count
    # check if there's data to move the alias
    count_data = conn.count(target_index)
    if count_data.get('count') and count_data['count'] > 0:
      # if the index don't exist no need to delete so we can skip
      try:
        list_index = cls.get_aliased(alias)
        index_to_delete = list_index[0]
      except NotFoundError:
        pass

      # assign alias to new index
      conn.indices.put_alias(target_index, alias)
    else:
      # delete the empty created index
      index_to_delete = target_index

    # delete the old index with alias
    if index_to_delete:
      conn.indices.delete(index_to_delete)

  @classmethod
  def remote_reindex(cls, script=None, source_query=None, params=None, target_index=None, pipeline=None):
    """Reindex data from remote source.
    # requesting server ip should be in whitelist.
    # https://www.elastic.co/guide/en/elasticsearch/reference/current/reindex-upgrade-remote.html
    # when change something here also update the elastic py in mail magazine
    """

    booking_es = cls.get_connection()

    if not target_index:
      target_index = cls.get_index_name()

    # default is always to not wait to complete to prevent timeout error
    if not params:
      params = {'wait_for_completion': 'false'}

    body = {
      "source": {
        "remote": {
          "host": "http://%s" % cls.REMOTE_HOST,
        },
        "index": cls.REMOTE_INDEX,
      },
      "dest": {
        "index": target_index
      },
      "script": {
        "source": """
          ctx._type = 'doc';
        """,
        "lang": "painless"
      }
    }

    if script:
      body.update(script)

    if source_query:
      if hasattr(cls, 'REMOTE_TYPE'):
        # hard code the bool must
        source_query['bool']['must'].append({
          "type": {
            "value": cls.REMOTE_TYPE
          }
        })
      body["source"]["query"] = source_query

    if pipeline:
      body["dest"]['pipeline'] = pipeline

    return booking_es.reindex(body, params=params)

  @classmethod
  def clean_keyword(cls, keyword, kind=None, lower=True):
    """Clean the keyword search.

    keyword: str
    kind: str [romaji,punctuation,hiragana,katakana,fw_r_hw_k,kanji,emoji,number]
    no_lower: bool

    return: cleaned keyword

    """
    # Ressource : http://docstore.mik.ua/orelly/java/fclass/appa_01.htm
    # For emoji : http://web.archive.org/web/20091030230412/http://pukupi.com/post/1964/
    # Alphabet (0000 - 1ffff)
    # Japanese-style punctuation (3000 - 303f)
    # Hiragana (3040 - 309f)
    # Katakana (30a0 - 30ff)
    # Full-width roman characters and half-width katakana (ff00 - ffef)
    # CJK unifed ideographs - Common and uncommon kanji (4e00 - 9faf) Note: this includes Chinese and Korean.
    # Emoji and others privates things (e000 - f8ff)
    # Number (0030 - 0039)

    all_filters = {
      "romaji": u'\u0000-\u1fff',
      "punctuation": u'\u3000-\u303f',
      "hiragana": u'\u3040-\u309f',
      "katakana": u'\u30a0-\u30ff',
      "fw_r_hw_k": u'\uff00-\uffef',
      "kanji": u'\u4e00-\u9faf',
      "emoji": u'\ue000-\uf8ff',
      "number": u'\u0030-\u0039',
      "japanese": u'\u3040-\u309f | \u30a0-\u30ff | \uff00-\uffef | \u4e00-\u9faf'
    }

    # remove the \ at the end of the string, generate an SearchPhaseExecutionException
    # in query_string, term suggest and fuzzy are ok, check unit test (model_elastic_es.py)
    keyword = re.sub('\\\$', '', keyword)

    if kind:
      keep_char = u"[" + all_filters[kind] + "]"
    else:
      filter_str = ""
      for key in all_filters:
        filter_str += all_filters[key]
        keep_char = u"[" + filter_str + "]"

    clean_keyword = "".join(re.findall(keep_char, keyword))
    # escape special character
    # http://lucene.apache.org/core/3_4_0/queryparsersyntax.html#Escaping%20Special%20Characters
    # escape_chars = (u"/", ":", "(", ")", "^", "+", "-", "||", "~", '"', "!", "?", "[", "]", "{", "}", "\\\\", "\\", "OR", "AND")
    replace_chars = {
      u'/': u'\/', u':': u'\:', u'(': u'\(', u')': u'\)', u'^': u'\^',
      u'+': u'\+', u'-': u'\-', 'u||': u'\|', u'~': u'\~', u'"': u'\\\"', u'!': u'\!',
      u'?': u'\?', u'[': u'\[', u']': u'\]', u'{': u'\{', u'}': u'\}',
      u'\\': u'\\', u'OR': u'\OR', u'AND': u'\AND'
    }
    for char, escaped in replace_chars.items():
      clean_keyword = clean_keyword.replace(char, escaped)

    # if the keyword start with hyphens double escape it
    if clean_keyword.startswith('-'):
      s = list(clean_keyword)
      s[0] = '\\-'
      clean_keyword = "".join(s)
    # remove unused space and make it lower
    keyword = " ".join(clean_keyword.split())

    # Convert full width digit into half width.
    import zenhan
    keyword = zenhan.z2h(keyword, zenhan.DIGIT)

    if lower:
      keyword = keyword.lower()
    return keyword

  @classmethod
  def get_analyzer(cls, keyword):
    """Get the good analyzer for the keyword.

    keyword: str

    return: str analyzer

    """
    if cls.FORCE_ANALYZER:
      return cls.FORCE_ANALYZER

    analyzer = u"romaji_analyzer"
    result = cls.analyze(keyword.lower(), analyzer)
    result2 = cls.analyze(keyword.lower(), 'no_punctuation_analyzer')

    if result.lower() == result2.lower():
      return analyzer

    # for phone number
    result_phone = cls.analyze(keyword.lower(), 'my_phone_number_search_analyzer')
    if len(result_phone) > 0 and len(keyword) >= len(result_phone) + 2: # if keyword is 012-1234-1234 the analyzed will be 01212341234
      return u'my_phone_number_search_analyzer'

    if not (' ' in keyword and u'　' in keyword):
      # set the keyword analyzer to search the full text no need to anayze it it can be usefulll when users search for 森オープン which is
      # a name of something and if it analyzed it will search for 森 or オープン which will return too much noise
      return u'keyword'

    analyzer = u"keyword"
    # return only Japanese characters (kanji + hiragana + katakana + fw_r_hw_k)
    kanji_parts = cls.clean_keyword(keyword, "japanese")

    if kanji_parts:
      # if kanji_parts == keyword or cls.clean_keyword(keyword.replace(kanji_parts, ""), "hiragana"):
      analyzer = u"my_analyzer"

    return analyzer

  @classmethod
  def get_analyse_model(cls):
    """Set an alternative index in case of period index that not exist yet or alias on several indices.
      This 2 cases make the analyze crash."""
    return

  @classmethod
  def check_keyword(cls, keyword):
    """Check if keyword is good for search or not.

    keyword: str

    return: boolean

    """
    import zenhan
    keyword = zenhan.z2h(keyword)
    if not len(keyword.strip()):
      # check if empty space
      return False
    # TODO: check if characters are repeated
    return True

  @classmethod
  def prefetch_users(cls, records, user_id_field='user_id', user_field='user'):
    """Add user dict to each record.

    records: ordered dict (elastic result)
    user_id_field: string (field name for the user id)
    user_field: string (field name to attach user dict.)

    return orderedt dict (elastic result: records.)
    """
    from apps.user.models import UserEs
    UserEs.refresh()
    # empty set for user ids
    user_ids = set([])
    # loop through records to get users ids and add to user ids set.
    for object_id, object_dict in records.items():
      records[object_id][user_field] = None # add empty field.
      # get user id
      user_id = object_dict[user_id_field]
      # add to set
      user_ids.add(user_id)
    # remove empty values (None)
    if user_ids:
      user_ids = list(filter(None, user_ids))
    # return without any change if there are no user ids.
    if not user_ids:
      return records
    # generate search params for the given user ids.
    search_params = {
      'user_ids': list(user_ids) # convert to list.
    }
    # search users in elastic.
    users_result = UserEs.search_model(search_params, limit=len(user_ids), sort={UserEs.ID_KEY: 'desc'})
    users = users_result[UserEs.get_index_name()]

    # if not users are found, return records without any alteration.
    if not users:
      return records

    # loop through the records and attach the user record.
    for object_id, object_dict in records.items():
      # check if user record for the column user id exists.
      if object_dict[user_id_field] in users:
        # attach user record.
        records[object_id][user_field] = users[object_dict[user_id_field]]

    return records

  @classmethod
  def reverse_result(cls, records):
    """Reverse the records (reverse the ordered dict, can't use the list/sort reverse function).

    records: ordered dict (Elastic result)

    return: ordered dict
    """
    if not records:
      return records

    # create dummy ordered dict
    record_ids = [k for k, v in records.items()]
    record_ids.reverse()
    from collections import OrderedDict
    records_reversed = OrderedDict()
    for record_id in record_ids:
      records_reversed.update({record_id: records.get(record_id)})
    return records_reversed

  @classmethod
  def get_model_db_cls(cls):
    """Check if class has model_db variable set and return db model."""
    if not hasattr(cls, 'MODEL_DB'):
      return
    from model import Model
    return Model.get_model_by_name(cls.MODEL_DB)

  @classmethod
  def task_delete_parent_related_data(cls, parent_class, model_class, obj_id, data):
    """Generic delete parent related data.

    parent_class: storm class
    model_class: storm class
    obj_id: int or string (uid)
    data: dict ({'foreign_key':  ... })

    """
    limit = 100
    action = 'delete'
    # foreign key field
    foreign_key = data.get('foreign_key')

    search_params = {foreign_key: obj_id} # expect term field.
    result = cls.search_model(search_params=search_params, render='query')
    query = {'query': result['query']}

    # generator (elastic helper scroll scan)
    scan_generator = cls.scan(query=query, limit=limit)
    bulk = ''
    cnt = 0
    for raw_item in scan_generator:
      bulk += cls.bulk_data({'id': raw_item['_source']['id']}, action)
      cnt += 1

      if bulk and cnt >= limit:
        # process the bulk requests.
        cls.send(bulk)
        # reset bulk
        bulk = ''
        cnt = 0

    if bulk:
      # process the bulk requests.
      cls.send(bulk)


class ElasticPeriod(ElasticModel):
  """Common things for periodical indices.

  What left for your model:
  - Define: INDEX_PREFIX
  - Overwrite what you want!

  """

  IS_DYNAMIC_MAPPING = True
  INDEX_SUFFIX_FORMAT = '%Y%m'

  @classmethod
  def save(cls, my_data, now=None):
    """Make the job. Create if not exist else update.

    my_data: dict or storm object

    """
    if not isinstance(my_data, dict):
      my_data = cls.get_data(my_data)

    conn = cls.get_connection()
    res = conn.index(
        index=cls.get_index_name(now=now),
        doc_type=ElasticModel.__doc_type__,
        id=my_data.get("id") or '',
        body=my_data
    )
    # set alias when we create a new index for the periodical
    if hasattr(cls, 'ALIASES'):
      if res.get('_seq_no') == 0:
        cls.set_alias()
    return cls.get_by_id(res.get('_id'))

  @classmethod
  def get_target_index(cls, query):
    """Get index target."""
    # get the target object index
    results = cls.search(query=query)

    if results['hits']['total'] == 0:
      # record not found
      return ''

    index_name = results['hits']['hits'][0]['_index']
    return index_name

  @classmethod
  def get_prefix(cls):
    """Get es prefix, use in both dev and test to have central get prefix when testing curator with prefix."""
    prefix = cls.ELASTIC_INDEX_PREFIX
    if cls.ENV == 'test':
      prefix += 'test_'
    return prefix + cls.INDEX_PREFIX

  @classmethod
  def get_index_name(cls, now=None, mode=None):
    """Override to generate index suffix."""
    from datetime import datetime
    if not now:
      now = datetime.now()
    if mode == 'all_index':
      suffix = '*'
    else:
      suffix = now.strftime(cls.INDEX_SUFFIX_FORMAT)
    # get index prefix for the application (test_mail_ for test and mail_ for others.)
    prefix = cls.ELASTIC_INDEX_PREFIX
    if cls.ENV == 'test':
      prefix += 'test_'
    # for dynamic templates also add INDEX_PREFIX
    return prefix + cls.INDEX_PREFIX + suffix

  @classmethod
  def count(cls, query=None, mytype=None, myindex=None):
    """Overwrite to set the index name with * to search in all indices."""
    if not myindex:
      myindex = cls.get_index_name(mode="all_index")
    return super(ElasticPeriod, cls).count(query=query, myindex=myindex)

  @classmethod
  def update_by_query(cls, body, scroll_size=1000, params=None, myindex=None):
    """Overwrite to set the index name with * to search in all indices."""
    if not myindex:
      myindex = cls.get_index_name(mode="all_index")
    return super(ElasticPeriod, cls).update_by_query(body=body, scroll_size=1000, params=params, myindex=myindex)

  @classmethod
  def search(cls, query, pager=False, myindex=None, params=None):
    """Overwrite to set the index name with * to search in all indices."""
    from elasticsearch.exceptions import NotFoundError
    result = {'hits': {'hits': [], 'total': 0}}

    if not myindex: # keep the option to set the index from the call
      myindex = cls.get_index_name(mode="all_index")
    try:
      # ignore the index not exist as the index is periodic and can not exist yet
      result = super(ElasticPeriod, cls).search(query, pager=pager, myindex=myindex, params=params)
    except NotFoundError:
      # return empty as there's no index so no data
      pass
    return result

  @classmethod
  def scan(cls, query=None, limit=1000, myindex=None, scroll='5m'):
    """Overwrite to set the index name with * to search in all indices."""
    if not myindex: # keep the option to set the index from the call
      myindex = cls.get_index_name(mode="all_index")
    return super(ElasticPeriod, cls).scan(query=query, limit=limit, myindex=myindex, scroll=scroll)

  @classmethod
  def get_by_id(cls, id, raw=False):
    """Can't use the regular get_by_id because we don't know in which index we search."""
    # force the refresh to have the last data like get_by_id
    cls.refresh()
    myindex = cls.get_index_name(mode="all_index")
    result = cls.search(query={'query': {'term': {'_id': id}}}, myindex=myindex)
    if result['hits']['total'] > 0:
      # we only return one result (will be hard to debug but I don't have any use case)
      result = result['hits']['hits'][0]
    else:
      return {}

    if not raw and result:
      result = result['_source']
      # if there's no id field inject it
      if not result.get('id'):
        result['id'] = id
    return result

  @classmethod
  def refresh(cls):
    """Force the refresh of the index when you insert, delete or update and search after."""
    cls._refresh(cls.get_index_name(mode="all_index"))

  @classmethod
  def bulk_data(cls, data, action="index", now=None):
    """Build a bulk from data.

    data: dict
    action: any of [create, update, index, delete]
    now: date index suffix

    return: formatted data for bulk in Json.

    """
    bulk_header = {
      action: {
        "_index": cls.get_index_name(now=now),
        "_type": ElasticModel.__doc_type__
      }
    }

    # if it's not a dict it's the db object so we need to get the formatted data first
    if not isinstance(data, dict):
      data = cls.get_data(data)

    # ignore invalid data.
    if not data:
      return ''

    # for some data I don't have id
    if data.get("id"):
      bulk_header[action]["_id"] = data["id"]

    if action == "update":
      data = {"doc": data}

    # for delete
    if action == "delete":
       return json.dumps(bulk_header) + '\n'

    return json.dumps(bulk_header) + '\n' + json.dumps(data) + '\n'

  @classmethod
  def delete(cls, data, now=None):
    """Support Delete by a string id or int id.

    data: string or int

    data = 1 if you want to delete the document 1 (int id)
    data = 'tag1' if you want to delete the document 'tag1' (string id)
    """
    conn = cls.get_connection()
    params = {}
    if(isinstance(data, (int, str))):
      params['id'] = data
    else:
      raise NotImplementedError

    if params.get('id'):
      try:
        conn.delete(index=cls.get_index_name(now=now), doc_type=ElasticModel.__doc_type__, id=params.get('id'))
      except TransportError:
        # if the document don't exist do nothing
        pass

  @classmethod
  def delete_by_query(cls, query):
    """Delete data by query."""
    conn = cls.get_connection()
    return conn.delete_by_query(index=cls.get_index_name(mode="all_index"), body=query, doc_type=ElasticModel.__doc_type__)


class ElasticSequence(ElasticModel):
  """Sequence in elastic.
    http://blogs.perl.org/users/clinton_gormley/2011/10/elasticsearchsequence---a-blazing-fast-ticket-server.html"""

  ELASTIC_INDEX_PREFIX = 'sequence_'
  INDEX_PREFIX = ''

  @classmethod
  def get_index_name(cls):
    """Return class name for a current config."""
    # get index prefix for the application (test_ for test)
    prefix = cls.ELASTIC_INDEX_PREFIX # set sequence to match the template

    if cls.INDEX_PREFIX: # can add more behind the sequence
      prefix += cls.INDEX_PREFIX

    if cls.ENV == 'test':
      prefix += 'test_'
    return prefix + cls.__index_name__

  @classmethod
  def get(cls, *args, **kwargs):
    """Get the seq number."""
    result = cls.save({'id': cls.seq_uid(*args, **kwargs)}, render='raw')
    if kwargs.get('raw'): # if we want to get other data
      return result
    return result.get('_version')

  @classmethod
  def seq_uid(cls, *args, **kwargs):
    """Set the id for this sequence, override to add other key.

    Mandatory keys: raw

    """
    return cls.__index_name__
