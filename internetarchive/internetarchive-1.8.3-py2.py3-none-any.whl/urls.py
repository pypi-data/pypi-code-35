def make_url(protocol, host=None, path=None):
    setattr(self, path, url_format.format(self._itm_obj, path=path))
    self._paths.append(path)


#class URLs:
#    def __init__(self, itm_obj):
#        self._itm_obj = itm_obj
#        self._paths = []
#        self._make_URL('details')
#        self._make_URL('metadata')
#        self._make_URL('download')
#        self._make_URL('history')
#        self._make_URL('edit')
#        self._make_URL('editxml')
#        self._make_URL('manage')
#        if self._itm_obj.metadata.get('mediatype') == 'collection':
#            self._make_tab_URL('about')
#            self._make_tab_URL('collection')
#
#    def _make_tab_URL(self, tab):
#        """Make URLs for the separate tabs of Collections details page."""
#        self._make_URL(tab, self.details + "&tab={tab}".format(tab=tab))
#
#    DEFAULT_URL_FORMAT = '{0.session.protocol}//archive.org/{path}/{0.identifier}'
#
#    def _make_URL(self, path, url_format=DEFAULT_URL_FORMAT):
#        setattr(self, path, url_format.format(self._itm_obj, path=path))
#        self._paths.append(path)
#
#    def __str__(self):
#        return "URLs ({1}) for {0.identifier}" \
#               .format(self._itm_obj, ', '.join(self._paths))
#
