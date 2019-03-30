# -*- coding: utf-8 -*-

import six.moves
import flask.sessions
import werkzeug.datastructures


class LazySession(six.moves.UserDict, flask.sessions.SessionMixin):
    callback_dict_class = werkzeug.datastructures.CallbackDict

    modified = False
    accessed = False

    def _notify_update(self, data):
        '''
        Mark this object as modified

        :param data: unused
        :type data: Any
        '''
        self.modified = True
        self.accessed = True

    def __init__(self, session_data_fnc, request=None):
        '''
        :param session_data_fnc: session data getter function
        :type session_data_fnc: Callable[[], Mapping[Any, Any]]
        :param request: request object
        :type request: Optional[flask.Request]
        '''
        self._data = None
        self._session_data_fnc = session_data_fnc
        self._request = request

    @property
    def data(self):
        '''
        :returns: returns inner session mapping object
        :rtype: Mapping[Any, Any]
        '''
        self.accessed = True
        if self._data is None:
            self._data = self.callback_dict_class(
                self._session_data_fnc(),
                self._notify_update
                )
        return self._data

    # TODO (on python2 drop): remove
    def __iter__(self):
        '''
        x.__iter__() <==> iter(x)

        :returns: keys in session mapping
        :rtype: Iterator[Any]
        '''
        return iter(self.data)
