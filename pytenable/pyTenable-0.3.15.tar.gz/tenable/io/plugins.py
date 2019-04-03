'''
plugins
=======

The following methods allow for interaction into the Tenable.io 
`plugins <https://cloud.tenable.com/api#/resources/plugins>`_ API endpoints.

Methods available on ``tio.plugins``:

.. rst-class:: hide-signature
.. autoclass:: PluginsAPI

    .. automethod:: families
    .. automethod:: family_details
    .. automethod:: plugin_details
'''
from .base import TIOEndpoint, TIOIterator
from datetime import date


class PluginIterator(TIOIterator):
    '''
    The plugins iterator provides a scalable way to work through plugin result
    sets of any size.  The iterator will walk through each page of data,
    returning one record at a time.  If it reaches the end of a page of
    records, then it will request the next page of information and then continue
    to return records from the next page (and the next, and the next) until the
    counter reaches the total number of records that the API has reported.

    Attributes:
        count (int): The current number of records that have been returned
        page (list): 
            The current page of data being walked through.  pages will be
            cycled through as the iterator requests more information from the
            API.
        page_count (int): The number of record returned from the current page.
        total (int): 
            The total number of records that exist for the current request.
    '''
    pass


class PluginsAPI(TIOEndpoint):
    def families(self):
        '''
        List the available plugin families.

        `plugins: families <https://cloud.tenable.com/api#/resources/plugins/families>`_

        Returns:
            list: List of plugin familiy resource records.

        Examples:
            >>> for family in tio.plugins.families():
            ...     pprint(family)
        '''
        return self._api.get('plugins/families').json()['families']

    def family_details(self, id):
        '''
        Retrieve the details for a specific plugin family.

        `plugins: family-details <https://cloud.tenable.com/api#/resources/plugins/family-details>`_

        Args:
            id (int): The plugin family unique identifier.

        Returns:
            dict: 
                Returns a dictionary stating the id, name, and plugins that are
                housed within the plugin family.

        Examples:
            >>> family = tio.plugins.family_details(1)
        '''
        return self._api.get('plugins/families/{}'.format(
                self._check('id', id, int)
        )).json()

    def plugin_details(self, id):
            '''
            Retrieve the details for a specific plugin.

            `plugins: plugin-details <https://cloud.tenable.com/api#/resources/plugins/plugin-details>`_

            Args:
                id (int): The plugin id for the requested plugin.

            Returns:
                dict:
                    A dictionary stating the id, name, family, and any other
                    relevant attributes associated to the plugin.

            Examples:
                >>> plugin = tio.plugins.plugin_details(19506)
                >>> pprint(plugin)
            '''
            return self._api.get('plugins/plugin/{}'.format(
                self._check('id', id, int))).json()

    def list(self, offset=None, limit=None, last_updated=None, pages=None):
        '''
        Get the listing of plugin details from Tenable.io.

        `plugins: list <>`_

        Args:
            limit (int, optional):
                The number of records to retrieve.  Default is 50
            offset (int, optional):
                The starting record to retrieve.  Default is 0.
            last_updated (date, optional):
                A datetime.date object stating when the threshold for the last
                updated field can be for a plugin.
            pages (int, optional):
                The total number of pages to request before stopping the
                iterator.
        Returns:
            PluginsIterator: 
                An iterator that handles the page management of the requested
                records.

        Examples:
            Getting the listing of all plugins:

            >>> for plugin in tio.plugins.list():
            ...     pprint(plugin)

            Retrieving all of the plugins updated since 2019-01-01:

            >>> for plugin in tio.plugins.list(last_updated=date(2019, 1, 1)):
            ...     pprint(plugin)
        '''
        return PluginIterator(self._api,
            _limit=self._check('limit', limit, int, default=1000),
            _offset=self._check('offset', offset, int, default=0),
            _query={
                'last_updated': self._check('last_updated', last_updated, date, 
                    default=date(1970, 1, 1)).strftime('%Y-%m-%d')
            },
            _pages_total=self._check('pages', pages, int),
            _path='plugins/plugin',
            _resource='plugin_details')