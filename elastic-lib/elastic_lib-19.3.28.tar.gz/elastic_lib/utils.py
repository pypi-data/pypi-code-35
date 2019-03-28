# source: http://epoz.org/blog/django-paginator-elasticsearch.html
# django: https://docs.djangoproject.com/en/1.11/topics/pagination/


class ElasticSearchPaginatorListException(Exception):
    pass


class ElasticSearchPaginatorResult(object):
    def __init__(self, result):
        self.result = result['hits']['hits']
        self._count = result['hits']['total']

    def count(self):
        return self._count

    def __len__(self):
        return self.count()

    def __getitem__(self, key):
        if not isinstance(key, slice):
            raise ElasticSearchPaginatorListException('key parameter in __getitem__ is not a slice instance')
        return self.result


class ElasticSearchPaginatorDict(object):
    """DEPRECATED WILL BE REMOVED DO NOT USE."""
    def __init__(self, records, count, reverse):
        self._records = records # dict
        self._count = count
        self._is_reverse = reverse

    def count(self):
        return self._count

    def __len__(self):
        return self.count()

    def __getitem__(self, key):
        if not isinstance(key, slice):
            raise ElasticSearchPaginatorListException('key parameter in __getitem__ is not a slice instance')
        # we already have the sileced data return all
        ret = list(self._records.values()) # return only values
        # reverse
        if self._is_reverse:
          ret.reverse()
        # raise
        return ret


class DictFactory(dict):

  KEEP_META = False # Flag if we want to keep the meta entry if defined in the factory

  def __init__(self, *args, **kwargs):
    """Initiate the object with the attributs defined in factory class."""
    kwargs = self.create(**kwargs)
    dict.__init__(self, *args, **kwargs)

  @classmethod
  def build(cls, **kwargs):
    """Build the dict and return it."""
    ret = {}

    attributs = cls._clean_attr()
    # build the dict and overwrite the default value defined in the factory by the kwargs set
    for one_attribut in attributs:
      if one_attribut in kwargs:
        value = kwargs[one_attribut]
      else:
        value = getattr(cls, one_attribut)
      ret.update({one_attribut: value})
    return ret

  @classmethod
  def _clean_attr(cls):
    """Clean the class attributs to build the dict."""
    # get the attributs of the factory model
    attributs = [i for i in cls.__dict__.keys() if not i.startswith('_')]
    # remove the meta key if exist and the mode don't use
    if not cls.KEEP_META and 'Meta' in attributs:
      attributs.remove('Meta')
    return attributs

  @classmethod
  def create(cls, **kwargs):
    """Overrtite if you can persiste the data."""
    raise NotImplementedError('canot persiste the dict.')

  @classmethod
  def create_batch(cls, nb_record, **kwargs):
    """Overrtite if you can persiste the data."""
    raise NotImplementedError('canot persiste the dict.')


class ElasticFactory(DictFactory):
  """FactoryBoy like for Elastic dict.

  http://factoryboy.readthedocs.io/en/latest/reference.html#factory.Factory._create
  """

  MAX_BULK_SIZE = 50 # depends on the content need to overwrite in the factory defintion add the attribut max_bulk_size in Meta
  KEEP_META = True # if we don't want that dict Factory remove the meta key from the attributs list

  @classmethod
  def build(cls, **kwargs):
    """Build the dict, set the object attribut and return it."""
    ret = dict()

    attributs = cls._clean_attr()
    # build the dict and overwrite the default value defined in the factory by the kwargs set
    for one_attribut in attributs:
      if one_attribut in kwargs:
        value = kwargs[one_attribut]
      else:
        value = getattr(cls, one_attribut)
      ret.update({one_attribut: value})
    return ret

  @classmethod
  def create(cls, **kwargs):
    """Save the dict and return it."""
    my_data = cls.build(**kwargs)
    factory_data = cls.Meta.model.save(my_data)
    if hasattr(cls.Meta.model, 'ALIASES'):
      cls.Meta.model.set_alias()
    return factory_data

  @classmethod
  def create_batch(cls, nb_record, **kwargs):
    """Create n records in elastic, using bulk.

    nb_record: int
    """
    model_class = cls.Meta.model
    ids = []
    if hasattr(cls.Meta, 'max_bulk_size'):
      max_bulk_size = cls.Meta.max_bulk_size
    else:
      max_bulk_size = cls.MAX_BULK_SIZE

    bulk = ''

    # force limit the nb of records
    if nb_record > max_bulk_size:
      nb_record = max_bulk_size

    for x in range(0, nb_record):
      bulk += model_class.bulk_data(cls.build(**kwargs))

    bulk_result = model_class.send(bulk)
    # get the ids
    for one_record in bulk_result['items']:
      ids.append(one_record['index']['_id'])
    model_class.refresh()
    # scan for the result and return the generator to loop throw
    query = {'_source': '*', 'query': {'terms': {'_id': ids}}}
    return model_class.scan(query, limit=len(ids))

  @classmethod
  def _clean_attr(cls):
    """Overwrite cause Meta is mandatory."""
    attributs = super()._clean_attr()
    # remove the Meta we use to get the model instance
    if 'Meta' not in attributs:
      raise NotImplementedError("You must define a Meta with a model attribut!")
    else:
      attributs.remove('Meta')
    return attributs
