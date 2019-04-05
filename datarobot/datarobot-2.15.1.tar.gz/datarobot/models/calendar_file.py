from datarobot.client import get_client, staticproperty
from datarobot.models.api_object import APIObject
from datarobot.models.sharing import SharingAccess
from datarobot.utils.pagination import unpaginate
from ..utils import encode_utf8_if_py2
import six
import os
import trafaret as t

from .. import errors
from datarobot.utils.waiters import wait_for_async_resolution


class CalendarFile(APIObject):
    """ Represents the data for a calendar file

    Attributes
    ----------
    id : str
        The id of the calendar file.
    calendar_start_date : str
        The earliest date in the calendar.
    calendar_end_date : str
        The last date in the calendar.
    created  : str
        The date this calendar was created, i.e. uploaded to DR.
    name : str
        The name of the calendar.
    num_event_types : int
        The number of different event types.
    num_events : int
        The number of events this calendar has.
    project_ids : list of strings
        A list containing the projectIds of the projects using this calendar.
    role : str
        The access role the user has for this calendar.
    """

    _base_url = 'calendars/'

    _upload_url = _base_url + 'fileUpload/'
    _calendar_url = _base_url + '{}/'
    _access_control_url = _calendar_url + 'accessControl/'

    _client = staticproperty(get_client)

    _converter = t.Dict({
        t.Key('calendar_end_date'): t.String,
        t.Key('calendar_start_date'): t.String,
        t.Key('created'): t.String,
        t.Key('id'): t.String,
        t.Key('name'): t.String,
        t.Key('num_event_types'): t.Int,
        t.Key('num_events'): t.Int,
        t.Key('project_ids'): t.List(t.String),
        t.Key('role'): t.String,
    }).ignore_extra('*')

    def __init__(self, calendar_end_date=None, calendar_start_date=None, created=None, id=None,
                 name=None, num_event_types=None, num_events=None, project_ids=None, role=None):
        self.calendar_end_date = calendar_end_date
        self.calendar_start_date = calendar_start_date
        self.created = created
        self.id = id
        self.name = name
        self.num_event_types = num_event_types
        self.num_events = num_events
        self.project_ids = project_ids
        self.role = role

    def __repr__(self):
        return encode_utf8_if_py2(u'{}({})'.format(self.__class__.__name__, self.id))

    def __eq__(self, other):
        """ Compares the relevant fields of two calendars to assess equality """
        vars1 = [self.__getattribute__(x) for x in [k.name for k in self._converter.keys]]
        vars2 = [other.__getattribute__(x) for x in [k.name for k in other._converter.keys]]
        return vars1 == vars2

    @classmethod
    def create(cls, file_path, calendar_name=None):
        """
        Creates a calendar using the given file.
        The provided file must be a CSV in the format:

        .. code-block:: text

            Date,   Event
            <date>, <event_type>,
            <date>, <event_type>,

        A header row is required.

        Parameters
        ----------
        file_path : string
            A string representing a path to a local csv file.
        calendar_name : string, optional
            A name to assign to the calendar. Defaults to the name of the file if not provided.

        Returns
        -------
        calendar_file : CalendarFile
            Instance with initialized data.

        Raises
        ------
        AsyncProcessUnsuccessfulError
            Raised if there was an error processing the provided calendar file.

        Examples
        --------
        .. code-block:: python

            # Creating a calendar with a specified name
            cal = dr.CalendarFile.create('/home/calendars/somecalendar.csv',
                                                     calendar_name='Some Calendar Name')
            cal.id
            >>> 5c1d4904211c0a061bc93013
            cal.name
            >>> Some Calendar Name

            # Creating a calendar without specifying a name
            cal = dr.CalendarFile.create('/home/calendars/somecalendar.csv')
            cal.id
            >>> 5c1d4904211c0a061bc93012
            cal.name
            >>> somecalendar.csv
        """

        # make sure it's a valid filename, and set the calendar name if not provided
        if isinstance(file_path, six.string_types) and os.path.isfile(file_path):
            if not calendar_name:
                calendar_name = os.path.basename(file_path)
        else:
            raise ValueError(
                u'The provided file does not exist: {}'.format(file_path)
            )
        try:
            calendar_name.encode('ascii')
        # Which exception we get here depends on whether the input was string or unicode
        # (we allow both).
        except (UnicodeEncodeError, UnicodeDecodeError):
            raise errors.IllegalFileName

        upload_response = cls._client.build_request_with_file(
            method='post',
            url=cls._upload_url,
            fname=calendar_name,
            file_path=file_path
        )
        new_calendar_url = wait_for_async_resolution(
            cls._client, upload_response.headers['Location'])

        return cls.from_location(new_calendar_url)

    @classmethod
    def get(cls, calendar_id):
        """
        Gets the details of a calendar, given the id.

        Parameters
        ----------
        calendar_id : str
            The identifier of the calendar.

        Returns
        -------
        calendar_file : CalendarFile
            The requested calendar.

        Raises
        ------
        DataError
            Raised if the calendar_id is invalid, i.e. the specified CalendarFile does not exist.

        Examples
        --------
        .. code-block:: python

            cal = dr.CalendarFile.get(some_calendar_id)
            cal.id
            >>> some_calendar_id
        """
        return cls.from_location(cls._calendar_url.format(calendar_id))

    @classmethod
    def list(cls, project_id=None, batch_size=None):
        """
        Gets the details of all calendars this user has view access for.

        Parameters
        ----------
        project_id : str, optional
            If provided, will filter for calendars associated only with the specified project.
        batch_size : int, optional
            The number of calendars to retrieve in a single API call. If specified, the client may
            make multiple calls to retrieve the full list of calendars. If not specified, an
            appropriate default will be chosen by the server.

        Returns
        -------
        calendar_list : list of :class:`CalendarFile <datarobot.CalendarFile>`
            A list of CalendarFile objects.

        Examples
        --------
        .. code-block:: python

            calendars = dr.CalendarFile.list()
            len(calendars)
            >>> 10
        """
        if project_id is not None:
            list_url = cls._base_url + '?projectId={}'.format(project_id)
        else:
            list_url = cls._base_url

        params = {}
        if batch_size is not None:
            params['limit'] = batch_size

        return [cls.from_server_data(entry)
                for entry in unpaginate(list_url, params, cls._client)]

    @classmethod
    def delete(cls, calendar_id):
        """
        Deletes the calendar specified by calendar_id.

        Parameters
        ----------
        calendar_id : str
            The id of the calendar to delete.
            The requester must have OWNER access for this calendar.

        Raises
        ------
        ClientError
            Raised if an invalid calendar_id is provided.

        Examples
        --------
        .. code-block:: python

            # Deleting with a valid calendar_id
            status_code = dr.CalendarFile.delete(some_calendar_id)
            status_code
            >>> 204
            dr.CalendarFile.get(some_calendar_id)
            >>> ClientError: Item not found
        """
        cls._client.delete(cls._calendar_url.format(calendar_id))

    @classmethod
    def update_name(cls, calendar_id, new_calendar_name):
        """
        Changes the name of the specified calendar to the specified name.
        The requester must have at least READ_WRITE permissions on the calendar.

        Parameters
        ----------
        calendar_id : str
            The id of the calendar to update.
        new_calendar_name : str
            The new name to set for the specified calendar.

        Returns
        -------
        status_code : int
            200 for success

        Raises
        ------
        ClientError
            Raised if an invalid calendar_id is provided.

        Examples
        --------
        .. code-block:: python

            response = dr.CalendarFile.update_name(some_calendar_id, some_new_name)
            response
            >>> 200
            cal = dr.CalendarFile.get(some_calendar_id)
            cal.name
            >>> some_new_name

        """
        try:
            new_calendar_name.encode('ascii')
        # Which exception we get here depends on whether the input was string or unicode
        # (we allow both).
        except (UnicodeEncodeError, UnicodeDecodeError):
            raise errors.IllegalFileName

        response_data = cls._client.patch(
            cls._calendar_url.format(calendar_id),
            data={'name': new_calendar_name}
        )
        return response_data.status_code

    @classmethod
    def share(cls, calendar_id, access_list):
        """
        Shares the calendar with the specified users, assigning the specified roles.

        Parameters
        ----------
        calendar_id : str
            The id of the calendar to update
        access_list:
            A list of dr.SharingAccess objects. Specify `None` for the role to delete a user's
            access from the specified CalendarFile. For more information on specific access
            levels, see the :ref:`sharing <sharing>` documentation.

        Returns
        -------
        status_code : int
            200 for success

        Raises
        ------
        ClientError
            Raised if unable to update permissions for a user.
        AssertionError
            Raised if access_list is invalid.

        Examples
        --------
        .. code-block:: python

            # assuming some_user is a valid user, share this calendar with some_user
            sharing_list = [dr.SharingAccess(some_user_username,
                                             dr.enums.SHARING_ROLE.READ_WRITE)]
            response = dr.CalendarFile.share(some_calendar_id, sharing_list)
            response.status_code
            >>> 200

            # delete some_user from this calendar, assuming they have access of some kind already
            delete_sharing_list = [dr.SharingAccess(some_user_username,
                                                    None)]
            response = dr.CalendarFile.share(some_calendar_id, delete_sharing_list)
            response.status_code
            >>> 200

            # Attempt to add an invalid user to a calendar
            invalid_sharing_list = [dr.SharingAccess(invalid_username,
                                                     dr.enums.SHARING_ROLE.READ_WRITE)]
            dr.CalendarFile.share(some_calendar_id, invalid_sharing_list)
            >>> ClientError: Unable to update access for this calendar

        """
        # ensure access_list is a list
        assert isinstance(access_list, list), "access_list must be a list"
        # ensure each item in access_list is a SharingAccess object
        assert all(isinstance(access, SharingAccess) for access in access_list), \
            "access_list must be a list of dr.SharingAccess objects"

        payload = {'users': [access.collect_payload() for access in access_list]}
        response_data = cls._client.patch(
            cls._access_control_url.format(calendar_id),
            data=payload,
            keep_attrs={'role'})
        return response_data.status_code

    @classmethod
    def get_access_list(cls, calendar_id, batch_size=None):
        """
        Retrieve a list of users that have access to this calendar.

        Parameters
        ----------
        calendar_id : str
            The id of the calendar to retrieve the access list for.
        batch_size : int, optional
            The number of access records to retrieve in a single API call. If specified, the client
            may make multiple calls to retrieve the full list of calendars. If not specified, an
            appropriate default will be chosen by the server.

        Returns
        -------
        access_control_list : list of :class:`SharingAccess <datarobot.SharingAccess>`
            A list of :class:`SharingAccess <datarobot.SharingAccess>` objects.

        Raises
        ------
        ClientError
            Raised if user does not have access to calendar or calendar does not exist.

        """

        params = {}
        if batch_size is not None:
            params['limit'] = batch_size
        url = cls._access_control_url.format(calendar_id)
        return [SharingAccess.from_server_data(datum)
                for datum in unpaginate(url, params, cls._client)]
