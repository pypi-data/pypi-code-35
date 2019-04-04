# Copyright 2019 StreamSets Inc.

"""Classes for SCH-related models.

This module provides implementations of classes with which users may interact in the course of
writing tests that exercise SCH functionality.
"""

import collections
import copy
import json
import logging
import requests
import urllib3
import uuid
from datetime import datetime
from functools import partial

import inflection

from .sdc import DataCollector as SdcDataCollector
from .sdc_models import PipelineBuilder as SdcPipelineBuilder, Stage
from .utils import SeekableList, MutableKwargs, update_acl_permissions, set_acl, get_params

logger = logging.getLogger(__name__)

json_to_python_style = lambda x: inflection.underscore(x)
python_to_json_style = lambda x: inflection.camelize(x, uppercase_first_letter=False)


class BaseModel:
    """Base class for Control Hub models that essentially just wrap a dictionary.

    Args:
        data (:obj:`dict`): The underlying JSON representation of the model.
        attributes_to_ignore (:obj:`list`, optional): A list of string attributes to mask from being handled
            by this class' __setattr__ method. Default: ``None``.
        attributes_to_remap (:obj:`dict`, optional): A dictionary of attributes to remap with the desired attributes
            as keys and the corresponding property name in the JSON representation as values. Default: ``None``.
        repr_metadata (:obj:`list`, optional): A list of attributes to use in the model's __repr__ string.
            Default: ``None``.
    """

    def __init__(self, data, attributes_to_ignore=None, attributes_to_remap=None, repr_metadata=None):
        super().__setattr__('_data', data)
        super().__setattr__('_attributes_to_ignore', attributes_to_ignore or [])
        super().__setattr__('_attributes_to_remap', attributes_to_remap or {})
        super().__setattr__('_repr_metadata', repr_metadata or [])

    def __getattr__(self, name):
        name_ = python_to_json_style(name)
        if name in self._attributes_to_remap:
            remapped_name = self._attributes_to_remap[name]
            return self._data[remapped_name]
        elif (name_ in self._data and
              name not in self._attributes_to_ignore and
              name not in self._attributes_to_remap.values()):
            return self._data[name_]
        raise AttributeError('Could not find attribute {}.'.format(name_))

    def __setattr__(self, name, value):
        name_ = python_to_json_style(name)
        if name in self._attributes_to_remap:
            remapped_name = self._attributes_to_remap[name]
            self._data[remapped_name] = value
        elif (name_ in self._data and
              name not in self._attributes_to_ignore and
              name not in self._attributes_to_remap.values()):
            self._data[name_] = value
        else:
            super().__setattr__(name, value)

    def __dir__(self):
        return sorted(list(dir(object))
                      + list(self.__dict__.keys())
                      + list(json_to_python_style(key)
                             for key in self._data.keys()
                             if key not in (list(self._attributes_to_remap.values())
                                            + self._attributes_to_ignore))
                      + list(self._attributes_to_remap.keys()))

    def __eq__(self, other):
        return self._data == other._data

    def __repr__(self):
        return '<{} ({})>'.format(self.__class__.__name__,
                                  ', '.join('{}={}'.format(key, getattr(self, key)) for key in self._repr_metadata))


class UiMetadataBaseModel(BaseModel):
    def __getattr__(self, name):
        name_ = python_to_json_style(name)
        if name in self._attributes_to_remap:
            remapped_name = self._attributes_to_remap[name]
            return self._data[remapped_name]['value']
        elif (name_ in self._data and
              name not in self._attributes_to_ignore and
              name not in self._attributes_to_remap.values()):
            return self._data[name_]['value']
        raise AttributeError('Could not find attribute {}.'.format(name_))

    def __setattr__(self, name, value):
        name_ = python_to_json_style(name)
        if name in self._attributes_to_remap:
            remapped_name = self._attributes_to_remap[name]
            self._data[remapped_name]['value'] = value
        elif (name_ in self._data and
              name not in self._attributes_to_ignore and
              name not in self._attributes_to_remap.values()):
            self._data[name_]['value'] = value
        else:
            super().__setattr__(name, value)


class ModelCollection:
    """Base class wrapper with Abstractions.

    Args:
        control_hub: An instance of :py:class:`streamsets.sdk.sch.ControlHub`.
    """

    def __init__(self, control_hub):
        self._control_hub = control_hub
        self._id_attr = 'id'

    def _get_all_results_from_api(self, **kwargs):
        """Used to get multiple (all) results from api.

        Args:
            Optional arguments to be passed to filter the results.

        Returns:
            A (:obj:`tuple`): of
                A :py:obj:`streamsets.sdk.utils.SeekableList` of inherited instances of
                :py:class:`streamsets.sdk.sch_models.BaseModel` and
                A (:obj:`dict`) of local variables not used in this function.
        """
        pass

    def __iter__(self):
        """Enables the list enumeration or iteration."""
        for item in self._get_all_results_from_api()[0]:
            yield item

    def __getitem__(self, i):
        """Enables the user to fetch items by index.

        Args:
            i (:obj:`int`): Index of the item.

        Returns:
            An inherited instance of :py:class:`streamsets.sdk.sch_models.BaseModel`.
        """
        return self._get_all_results_from_api()[0][i]

    def __len__(self):
        """Provides length (count) of items.

        Returns:
            A :py:obj:`int` object
        """
        return len(self._get_all_results_from_api()[0])

    def __contains__(self, item_given):
        """Checks if given item is in the list of items by comparing the ids.

        Returns:
            A :py:obj:`boolean` object
        """
        for item in self:
            if getattr(item, self._id_attr) == getattr(item_given, self._id_attr):
                return True
        return False

    def get(self, **kwargs):
        """
        Args:
            **kwargs: Optional arguments to be passed to filter the results offline.

        Returns:
            An inherited instance of :py:class:`streamsets.sdk.sch_models.BaseModel`.
        """
        result, new_kwargs = self._get_all_results_from_api(**kwargs)
        return result.get(**new_kwargs)

    def get_all(self, **kwargs):
        """
        Args:
            **kwargs: Optional other arguments to be passed to filter the results offline.

        Returns:
            A :py:obj:`streamsets.sdk.utils.SeekableList` of inherited instances of
            :py:class:`streamsets.sdk.sch_models.BaseModel`.
        """
        result, new_kwargs = self._get_all_results_from_api(**kwargs)
        return result.get_all(**new_kwargs)


class ACL(BaseModel):
    """Represents an ACL.

    Args:
        acl (:obj:`dict`): JSON representation of an ACL.
        control_hub (:py:class:`streamsets.sdk.sch.ControlHub`): Control Hub object.

    Attributes:
        permissions (:py:class:`streamsets.sdk.sch_models.Permissions`): A Collection of Permissions.
    """
    _ATTRIBUTES_TO_REMAP = {'resource_id': 'resourceId',
                            'resource_owner': 'resourceOwner',
                            'resource_created_time': 'resourceCreatedTime',
                            'resource_type': 'resourceType',
                            'last_modified_by': 'lastModifiedBy',
                            'last_modified_on': 'lastModifiedOn'}
    _ATTRIBUTES_TO_IGNORE = ['permissions']
    _REPR_METADATA = ['resource_id', 'resource_type']

    def __init__(self, acl, control_hub):
        super().__init__(acl,
                         attributes_to_remap=ACL._ATTRIBUTES_TO_REMAP,
                         attributes_to_ignore=ACL._ATTRIBUTES_TO_IGNORE,
                         repr_metadata=ACL._REPR_METADATA)
        self.permissions = SeekableList(Permission(permission,
                                                   self.resource_type,
                                                   control_hub.api_client) for permission in self._data['permissions'])
        self._control_hub = control_hub

    def __getitem__(self, key):
        return getattr(self, key)

    def __len__(self):
        return len(self._data)

    @property
    def permission_builder(self):
        """Get a permission builder instance with which a pipeline can be created.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ACLPermissionBuilder`.
        """
        permission = {property: None
                      for property in self._control_hub._job_api['definitions']['PermissionJson']['properties']}

        return ACLPermissionBuilder(permission=permission, acl=self)

    def add_permission(self, permission):
        """Add new permission to the ACL.

        Args:
            permission (:py:class:`streamsets.sdk.sch_models.Permission`): A permission object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`
        """
        self._data['permissions'].append(permission._data)
        return set_acl(self._control_hub.api_client, self.resource_type, self.resource_id, self._data)

    def remove_permission(self, permission):
        """Remove a permission from ACL.

        Args:
            permission (:py:class:`streamsets.sdk.sch_models.Permission`): A permission object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`
        """
        permissions = self._data['permissions']
        self._data['permissions'] = [perm for perm in permissions if perm['subjectId'] != permission.subject_id]
        return set_acl(self._control_hub.api_client, self.resource_type, self.resource_id, self._data)


class ACLPermissionBuilder():
    """Class to help build the ACL permission.

    Args:
        permission (:py:class:`streamsets.sdk.sch_models.Permission`): A permission object.
        acl (:py:class:`streamsets.sdk.sch_models.ACL`): An ACL object.
    """

    def __init__(self, permission, acl):
        self._permission = permission
        self._acl = acl

    def build(self, subject_id, subject_type, actions):
        """Method to help build the ACL permission.

        Args:
            subject_id (:obj:`str`): Id of the subject e.g. 'test@test'.
            subject_type (:obj:`str`): Type of the subject e.g. 'USER'.
            actions (:obj:`list`): A list of actions of type :obj:`str` e.g. ['READ', 'WRITE', 'EXECUTE'].

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Permission`.
        """
        self._permission.update({'resourceId': self._acl.resource_id,
                                 'subjectId': subject_id,
                                 'subjectType': subject_type,
                                 'actions': actions})
        return Permission(self._permission, self._acl.resource_type, self._acl._control_hub.api_client)


class Permission(BaseModel):
    """A container for a permission.

    Args:
        permission (:obj:`dict`): A Python object representation of a permission.
        resource_type (:obj:`str`): String representing the type of resource e.g. 'JOB', 'PIPELINE'.
        api_client (:py:class:`streamsets.sdk.sch_api.ApiClient`): An instance of ApiClient.

    Attributes:
        resource_id (:obj:`str`): Id of the resource e.g. Pipeline or Job.
        subject_id (:obj:`str`): Id of the subject e.g. user id ``'admin@admin'``.
        subject_type (:obj:`str`): Type of the subject e.g. ``'USER'``.
        last_modified_by (:obj:`str`): User who last modified this permission e.g. ``'admin@admin'``.
        last_modified_on (:obj:`int`): Timestamp at which this permission was last modified e.g. ``1550785079811``.
    """
    _ATTRIBUTES_TO_REMAP = {'resource_id': 'resourceId',
                            'subject_id': 'subjectId',
                            'subject_type': 'subjectType',
                            'last_modified_by': 'lastModifiedBy',
                            'last_modified_on': 'lastModifiedOn'}
    _ATTRIBUTES_TO_IGNORE = ['resource_type', 'api_client']
    _REPR_METADATA = ['resource_id', 'subject_type', 'subject_id']

    def __init__(self, permission, resource_type, api_client):
        super().__init__(permission,
                         attributes_to_remap=Permission._ATTRIBUTES_TO_REMAP,
                         attributes_to_ignore=Permission._ATTRIBUTES_TO_IGNORE,
                         repr_metadata=Permission._REPR_METADATA)
        self._resource_type = resource_type
        self._api_client = api_client

    def __setattr__(self, key, value):
        if key == 'actions':
            self._data[key] = value
            update_acl_permissions(self._api_client, self._resource_type, self._data)
        self.__dict__[key] = value


class UserBuilder:
    """Class with which to build instances of :py:class:`streamsets.sdk.sch_models.User`.

    Instead of instantiating this class directly, most users should use
        :py:meth:`streamsets.sdk.sch.ControlHub.get_user_builder`.

    Args:
        user (:obj:`dict`): Python object built from our Swagger UserJson definition.
        roles (:obj:`dict`): A mapping of role IDs to role labels.
    """

    def __init__(self, user, roles):
        self._user = user
        self._roles = roles

    def build(self, id, display_name, email_address, saml_user_name=None):
        """Build the user.

        Args:
            id (:obj:`str`): User Id.
            display_name (:obj:`str`): User display name.
            email_address (:obj:`str`): User Email Address.
            saml_user_name (:obj:`str`, optional): Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.User`.
        """
        self._user.update({'id': id,
                           'name': display_name,
                           'email': email_address,
                           # Following logic from https://git.io/fNsoQ.
                           'nameInOrg': saml_user_name or id})
        return User(user=self._user, roles=self._roles)


class User(BaseModel):
    """Model for User.

    Args:
        user (:obj:`dict`): JSON representation of User.
        roles (:obj:`dict`): A mapping of role IDs to role labels.

    Attributes:
        active (:obj:`bool`): Whether the user is active or not.
        created_by (:obj:`str`): Creator of this user.
        created_on (:obj:`str`): Creation time of this user.
        display_name (:obj:`str`): Display name of this user.
        email_address (:obj:`str`): Email address of this user.
        id (:obj:`str`): Id of this user.
        groups (:obj:`list`): Groups this user belongs to.
        last_modified_by (:obj:`str`): User last modified by.
        last_modified_on (:obj:`str`): User last modification time.
        password_expires_on (:obj:`str`): User's password expiration time.
        password_system_generated (:obj:`bool`): Whether User's password is system generated or not.
        roles (:obj:`set`): A set of role labels.
        saml_user_name (:obj:`str`): SAML username of user.
    """
    _ATTRIBUTES_TO_IGNORE = ['destroyer', 'organization', 'roles', 'userDeleted']
    _ATTRIBUTES_TO_REMAP = {'created_by': 'creator',
                            'email_address': 'email',
                            'display_name': 'name',
                            'saml_user_name': 'nameInOrg',
                            'password_expires_on': 'passwordExpiryTime',
                            'password_system_generated': 'passwordGenerated'}
    _REPR_METADATA = ['id', 'display_name']

    # Jetty requires ever SCH user to have the 'user' role, which is hidden in the UI. We'll do the same.
    _ROLES_TO_HIDE = ['user']

    def __init__(self, user, roles):
        super().__init__(user,
                         attributes_to_ignore=User._ATTRIBUTES_TO_IGNORE,
                         attributes_to_remap=User._ATTRIBUTES_TO_REMAP,
                         repr_metadata=User._REPR_METADATA)
        self._roles = roles

    @property
    def roles(self):
        return {self._roles[role] for role in self._data.get('roles', []) if role not in User._ROLES_TO_HIDE}

    @roles.setter
    def roles(self, value):
        # We reverse the _roles dictionary to let this setter deal with role labels while still writing role ids.
        role_label_to_id = {role_label: role_id for role_id, role_label in self._roles.items()}

        value_ = value if isinstance(value, list) else [value]
        self._data['roles'] = list({role_label_to_id[role] for role in value_} | set(User._ROLES_TO_HIDE))


class Users(ModelCollection):
    """Collection of :py:class:`streamsets.sdk.sch_models.User` instances.

    Args:
        control_hub: An instance of :py:class:`streamsets.sdk.sch.ControlHub`.
        roles (:obj:`dict`): A mapping of role IDs to role labels.
        organization (:obj:`str`): Organization ID.
    """

    def __init__(self, control_hub, roles, organization):
        super().__init__(control_hub)
        self._roles = roles
        self._organization = organization

    def _get_all_results_from_api(self, id=None, organization=None, **kwargs):
        """
        Args:
            id (:obj:`str`)
            organization (:obj:`str`)
            kwargs: Other optional arguments

        Returns:
            A (:obj:`tuple`): of
                A :py:class:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.User` instances
                and
                A (:obj:`dict`) of local variables not used in this function.
        """
        if organization is None:
            organization = self._organization
        if id is not None:
            try:
                return SeekableList([User(self._control_hub.api_client.get_user(org_id=organization,
                                                                                user_id=id).response.json(),
                                          self._roles)]), kwargs
            except requests.exceptions.HTTPError:
                raise ValueError('User (id={}) not found'.format(id))
        return SeekableList(User(user, self._roles)
                            for user in
                            self._control_hub.api_client.get_all_users(organization).response.json()), kwargs


class Group(BaseModel):
    """Model for Group.

    Args:
        group (:obj:`dict`): A Python object representation of Group.
    """
    _REPR_METADATA = ['id', 'name']

    def __init__(self, group):
        super().__init__(group, repr_metadata=Group._REPR_METADATA)


class OrganizationBuilder:
    """Class with which to build instances of :py:class:`streamsets.sdk.sch_models.Organization`.

    Instead of instantiating this class directly, most users should use
        :py:meth:`streamsets.sdk.sch.ControlHub.get_organization_builder`.

    Args:
        organization (:obj:`dict`): Python object built from our Swagger UserJson definition.
    """

    def __init__(self, organization, organization_admin_user):
        self._organization = organization
        self._organization_admin_user = organization_admin_user

    def build(self, id, name,
              admin_user_id, admin_user_display_name, admin_user_email_address):
        """Build the organization.

        Args:
            id (:obj:`str`): Organization ID.
            name (:obj:`str`): Organization name.
            admin_user_id (:obj:`str`): User Id of the admin of this organization.
            admin_user_display_name (:obj:`str`): User display name of admin of this organization.
            admin_user_email_address (:obj:`str`): User email address of admin of this organization.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Organization`.
        """
        self._organization.update({'id': id,
                                   'name': name,
                                   'primaryAdminId': admin_user_id})
        self._organization_admin_user.update({'id': admin_user_id,
                                              'name': admin_user_display_name,
                                              'email': admin_user_email_address,
                                              'organization': id})
        return Organization(self._organization, self._organization_admin_user)


class Organization(BaseModel):
    """Model for Organization.

    Args:
        organization (:obj:`str`): Organization Id.
        organization_admin_user (:obj:`str`, optional): Default: ``None``.
        api_client (:py:obj:`streamsets.sdk.sch_api.ApiClient`, optional): Default: ``None``.
    """
    _ATTRIBUTES_TO_IGNORE = ['configuration', 'passwordExpiryTimeInMillis', ]
    _ATTRIBUTES_TO_REMAP = {'admin_user_id': 'primaryAdminId',
                            'created_by': 'creator',
                            'saml_intergration_enabled': 'externalAuthEnabled'}
    _REPR_METADATA = ['id', 'name']

    def __init__(self, organization, organization_admin_user=None, api_client=None):
        super().__init__(organization,
                         attributes_to_ignore=Organization._ATTRIBUTES_TO_IGNORE,
                         attributes_to_remap=Organization._ATTRIBUTES_TO_REMAP,
                         repr_metadata=Organization._REPR_METADATA)
        self._organization_admin_user = organization_admin_user
        self._api_client = api_client

    @property
    def default_user_password_expiry_time_in_days(self):
        return self._data['passwordExpiryTimeInMillis'] / 86400000  # 1 d => ms

    @default_user_password_expiry_time_in_days.setter
    def default_user_password_expiry_time_in_days(self, value):
        self._data['passwordExpiryTimeInMillis'] = value * 86400000

    @property
    def configuration(self):
        configuration = self._api_client.get_organization_configuration(self.id).response.json()

        # Some of the config names are a bit long, so shorten them slightly...
        ID_TO_REMAP = {'accountType': 'Organization account type',
                       'contractExpirationTime': 'Timestamp of the contract expiration',
                       'trialExpirationTime': 'Timestamp of the trial expiration'}
        return Configuration(configuration=configuration,
                             update_callable=self._api_client.update_organization_configuration,
                             update_callable_kwargs=dict(org_id=self.id),
                             id_to_remap=ID_TO_REMAP)

    @configuration.setter
    def configuration(self, value):
        self._api_client.update_organization_configuration(self.id, value._data)


class Organizations(ModelCollection):
    """Collection of :py:class:`streamsets.sdk.sch_models.Organization` instances."""

    def _get_all_results_from_api(self, **kwargs):
        """
        Args:
            kwargs: optional arguments

        Returns:
            A (:obj:`tuple`): of
                A :py:obj:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.Organization`
                instances.
                and
                A (:obj:`dict`) of local variables not used in this function.
        """
        return SeekableList(Organization(organization, api_client=self._control_hub.api_client)
                            for organization in
                            self._control_hub.api_client.get_all_organizations().response.json()), kwargs


class Configuration:
    """A dictionary-like container for getting and setting configuration values.

    Args:
        configuration (:obj:`dict`): JSON object representation of configuration.
        update_callable (optional): A callable to which ``self._data`` will be passed as part of ``__setitem__``.
        update_callable_kwargs (:obj:`dict`, optional): A dictionary of kwargs to pass (along with a body)
            to the callable.
        id_to_remap (:obj:`dict`, optional): A dictionary mapping configuration IDs to human-readable container keys.
    """

    def __init__(self, configuration, update_callable=None, update_callable_kwargs=None, id_to_remap=None):
        self._data = configuration
        self._update_callable = update_callable
        self._update_callable_kwargs = update_callable_kwargs or {}
        self._id_to_remap = id_to_remap or {}

    def __getitem__(self, key):
        for config in self._data:
            if config['name'] == key or self._id_to_remap.get(config['id']) == key:
                break
        else:
            raise KeyError(key)
        if config['type'] == 'boolean':
            return json.loads(config['value'])
        elif config['type'] == 'integer':
            return int(config['value'])
        else:
            return config['value']

    def __setitem__(self, key, value):
        for config in self._data:
            if config['name'] == key or self._id_to_remap.get(config['id']) == key:
                break
        else:
            raise KeyError(key)
        config['value'] = value
        if self._update_callable:
            kwargs = dict(body=[config])
            kwargs.update(self._update_callable_kwargs)
            self._update_callable(**kwargs)

    def __repr__(self):
        configs = {}
        for config in self._data:
            key = self._id_to_remap.get(config['id']) or config['name']
            if config['type'] == 'boolean':
                value = json.loads(config['value'])
            elif config['type'] == 'integer':
                value = int(config['value'])
            else:
                value = config['value']
            configs[key] = value
        return '{{{}}}'.format(', '.join("'{}': {}".format(k, v) for k, v in configs.items()))


class DataCollector(BaseModel):
    """Model for Data Collector.

    Attributes:
        execution_mode (:obj:`bool`): ``True`` for Edge and ``False`` for SDC.
        id (:obj:`str`): Data Collectort id.
        labels (:obj:`list`): Labels for Data Collector.
        last_validated_on (:obj:`str`): Last validated time for Data Collector.
        reported_labels (:obj:`list`): Reported labels for Data Collector.
        url (:obj:`str`): Data Collector's url.
        version (:obj:`str`): Data Collector's version.
    """
    _ATTRIBUTES_TO_IGNORE = ['offsetProtocolVersion', 'edge']
    _ATTRIBUTES_TO_REMAP = {'execution_mode': 'edge',
                            'last_validated_on': 'lastReportedTime',
                            'url': 'httpUrl'}
    _REPR_METADATA = ['accessible', 'id', 'url']

    def __init__(self, data_collector, control_hub):
        super().__init__(data_collector,
                         attributes_to_ignore=DataCollector._ATTRIBUTES_TO_IGNORE,
                         attributes_to_remap=DataCollector._ATTRIBUTES_TO_REMAP,
                         repr_metadata=DataCollector._REPR_METADATA)
        self._control_hub = control_hub

    @property
    def accessible(self):
        """Returns a :obj:`bool` for whether the Data Collector instance is accessible."""
        try:
            # We disable InsecureRequestWarning and disable SSL certificate verification to enable self-signed certs.
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            requests.get(self.http_url, verify=False)
            return True
        except requests.exceptions.ConnectionError:
            return False

    @property
    def attributes(self):
        """Returns a :obj:`dict` of Data Collector attributes."""
        return self._component['attributes']

    @property
    def attributes_updated_on(self):
        return self._component['attributesUpdatedOn']

    @property
    def authentication_token_generated_on(self):
        return self._component['authTokenGeneratedOn']

    @property
    def instance(self):
        # Disable SSL cert verification to enable use of self-signed certs.
        SdcDataCollector.VERIFY_SSL_CERTIFICATES = False
        return SdcDataCollector(self.url, control_hub=self._control_hub)

    @property
    def registered_by(self):
        return self._component['registeredBy']

    @property
    def acl(self):
        """Get DataCollector ACL.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ACL`.
        """
        return ACL(self._control_hub.api_client.get_sdc_acl(sdc_id=self.id).response.json(), self._control_hub)

    @acl.setter
    def acl(self, sdc_acl):
        """Update DataCollector ACL.

        Args:
            sdc_acl (:py:class:`streamsets.sdk.sch_models.ACL`): The sdc ACL instance.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        return self._control_hub.api_client.set_sdc_acl(sdc_id=self.id, sdc_acl_json=sdc_acl._data)


class DataCollectors(ModelCollection):
    """Collection of :py:class:`streamsets.sdk.sch_models.DataCollector` instances.

    Args:
        control_hub (:py:class:`streamsets.sdk.sch.ControlHub`): Control Hub object.
    """

    def _get_all_results_from_api(self, id=None, **kwargs):
        """
        Args:
            id (:obj:`str`): id of DataCollector.
            **kwargs: Optional other arguments to be passed to filter the results offline.

        Returns:
            A (:obj:`tuple`): of
                A :py:obj:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.DataCollector`
                instances and
                A (:obj:`dict`) of local variables not used in this function.
        """
        if id is None:
            return (SeekableList(DataCollector(data_collector, self._control_hub)
                                 for data_collector in
                                 self._control_hub.api_client.get_all_registered_sdcs(organization=None,
                                                                                      edge=None,
                                                                                      label=None,
                                                                                      version=None,
                                                                                      offset=None,
                                                                                      len_=None,
                                                                                      order_by=None,
                                                                                      order=None).response.json()),
                    kwargs)
        try:
            return SeekableList([DataCollector(self._control_hub.api_client.get_sdc(id).response.json(),
                                               self._control_hub)]), kwargs
        except requests.exceptions.HTTPError:
            raise ValueError('DataCollector (id={}) not found'.format(id))


class PipelineBuilder(SdcPipelineBuilder):
    """Class with which to build instances of :py:class:`streamsets.sdk.sch_models.Pipeline`.

    Instead of instantiating this class directly, most users should use
        :py:meth:`streamsets.sdk.sch.ControlHub.get_user_builder`.

    Args:
        pipeline (:obj:`dict`): Python object built from our Swagger PipelineJson definition.
        data_collector_pipeline_builder (:py:class:`streamsets.sdk.sdc_models.PipelineBuilder`): Data Collector Pipeline
                                                                                                 Builder object.
    """

    def __init__(self, pipeline, data_collector_pipeline_builder):
        super().__init__(data_collector_pipeline_builder._pipeline,
                         data_collector_pipeline_builder._definitions)
        self._sch_pipeline = pipeline

    def build(self, title='Pipeline'):
        sdc_pipeline = super().build(title=title)
        sch_pipeline = Pipeline(pipeline=self._sch_pipeline,
                                builder=self,
                                pipeline_definition=sdc_pipeline._data['pipelineConfig'],
                                rules_definition=sdc_pipeline._data['pipelineRules'])
        sch_pipeline.name = title
        return sch_pipeline


class Pipeline(BaseModel):
    """Model for Pipeline.

    Args:
        pipeline (:obj:`dict`): Pipeline in JSON format.
        builder (:py:class:`streamsets.sdk.sch_models.PipelineBuilder`): Pipeline Builder object.
        pipeline_definition (:obj:`dict`): Pipeline Definition in JSON format.
        rules_definition (:obj:`dict`): Rules Definition in JSON format.
        control_hub (:py:class:`streamsets.sdk.sch.ControlHub`): ControlHub object.
    """
    _REPR_METADATA = ['pipeline_id', 'commit_id', 'name', 'version']
    _ATTRIBUTES_TO_REMAP = {'Labels': 'pipelineLabels'}

    def __init__(self, pipeline, builder, pipeline_definition, rules_definition, control_hub=None):
        super().__init__(pipeline,
                         repr_metadata=Pipeline._REPR_METADATA,
                         attributes_to_remap=Pipeline._ATTRIBUTES_TO_REMAP)
        self._builder = builder
        self._pipeline_definition = pipeline_definition
        self._rules_definition = rules_definition
        self._control_hub = control_hub

    @property
    def acl(self):
        """Get pipeline ACL.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ACL`.
        """
        return ACL(self._control_hub.api_client.get_pipeline_acl(pipeline_id=self.pipeline_id).response.json(), self._control_hub)

    @acl.setter
    def acl(self, pipeline_acl):
        """Update pipeline ACL.

        Args:
            pipeline_acl (:py:class:`streamsets.sdk.sch_models.ACL`): Pipeline ACL in JSON format.

        Returns:
            An instance of :py:class:`streamsets.sdc_api.Command`.
        """
        return self._control_hub.api_client.set_pipeline_acl(pipeline_id=self.pipeline_id, pipeline_acl_json=pipeline_acl._data)


class Pipelines(ModelCollection):
    """Collection of :py:class:`streamsets.sdk.sch_models.Pipeline` instances.

    Args:
        control_hub: An instance of :py:class:`streamsets.sdk.sch.ControlHub`.
        organization (:obj:`str`): Organization Id.
    """

    def __init__(self, control_hub, organization):
        super().__init__(control_hub)
        self._organization = organization
        self._id_attr = 'pipeline_id'

    def _get_all_results_from_api(self, organization=None, label=None, template=False, **kwargs):
        """Args offset, len, order_by, order, system, filter_text, only_published, execution_modes are not exposed
        directly as arguments because of their limited use by normal users but, could still be specified just like any
        other args with the help of kwargs.

        Args:
            organization (:obj:`str`): Organization id of pipeline.
            label (:obj:`str`): Label of pipeline
            template (:obj:`boolean`): Indicate if requesting pipeline templates or pipelines.
            **kwargs: Optional arguments to be passed to filter the results offline.

        Returns:
            A (:obj:`tuple`): of
                A :py:obj:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.Pipeline`
                instances and
                A (:obj:`dict`) of local variables not used in this function.
        """
        kwargs_defaults = {'offset': None, 'len': None, 'order_by': None, 'order': None, 'system': None,
                           'filter_text': None, 'only_published': None, 'execution_modes': None}
        kwargs_instance = MutableKwargs(kwargs_defaults, kwargs)
        kwargs_unioned = kwargs_instance.union()
        if label is not None:
            label_id_org = self._organization if organization is None else organization
            pipeline_label_id = '{}:{}'.format(label, label_id_org)
        else:
            pipeline_label_id = None
        if template:
            pipeline_commit_ids = [pipeline['commitId']
                                   for pipeline in self._control_hub.api_client.return_all_pipeline_templates(
                                    pipeline_label_id=pipeline_label_id,
                                    offset=kwargs_unioned['offset'],
                                    len=kwargs_unioned['len'],
                                    order_by=kwargs_unioned['order_by'],
                                    order=kwargs_unioned['order'],
                                    system=kwargs_unioned['system'],
                                    filter_text=kwargs_unioned['filter_text'],
                                    execution_modes=kwargs_unioned['execution_modes']).response.json()['data']]
        else:
            pipeline_commit_ids = [pipeline['commitId']
                                   for pipeline in self._control_hub.api_client.return_all_pipelines(
                                    organization=organization,
                                    pipeline_label_id=pipeline_label_id,
                                    offset=kwargs_unioned['offset'],
                                    len=kwargs_unioned['len'],
                                    order_by=kwargs_unioned['order_by'],
                                    order=kwargs_unioned['order'],
                                    system=kwargs_unioned['system'],
                                    filter_text=kwargs_unioned['filter_text'],
                                    only_published=kwargs_unioned['only_published'],
                                    execution_modes=kwargs_unioned['execution_modes']).response.json()['data']]
        if pipeline_commit_ids:
            result = SeekableList(Pipeline(pipeline=pipeline,
                                           builder=None,
                                           pipeline_definition=json.loads(pipeline['pipelineDefinition']),
                                           rules_definition=json.loads(pipeline['currentRules']['rulesDefinition']),
                                           control_hub=self._control_hub)
                                  for pipeline
                                  in self._control_hub.api_client.get_pipelines_commit(
                                    body=pipeline_commit_ids).response.json())
        else:
            result = SeekableList()
        kwargs_unused = kwargs_instance.subtract()
        return result, kwargs_unused


class JobBuilder:
    """Class with which to build instances of :py:class:`streamsets.sdk.sch_models.Job`.

    Instead of instantiating this class directly, most users should use
        :py:meth:`streamsets.sdk.sch.ControlHub.get_job_builder`.

    Args:
        job (:obj:`dict`): Python object built from our Swagger JobJson definition.
    """

    def __init__(self, job, control_hub):
        self._job = job
        self._control_hub = control_hub

    def build(self, job_name, pipeline, pipeline_commit_or_tag=None):
        """Build the job.

        Args:
            job_name (:obj:`str`): Name of the job.
            pipeline (:py:obj:`streamsets.sdk.sch_models.Pipeline`): Pipeline object.
            pipeline_commit_or_tag (:obj:`str`, optional): Default: ``None``, which resolves to the latest pipeline
                commit.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Job`.
        """
        self._job.update({'name': job_name,
                          'pipelineCommitId': pipeline_commit_or_tag or pipeline.commit_id,
                          'pipelineCommitLabel': 'v{}'.format(pipeline.version),
                          'pipelineId': pipeline.pipeline_id,
                          'pipelineName': pipeline.name,
                          'rulesId': pipeline.current_rules['id']})
        return Job(job=self._job, control_hub=self._control_hub)


class Job(BaseModel):
    """Model for Job.

    Attributes:
        commit_id (:obj:`str`): Pipeline commit id.
        commit_label (:obj:`str`): Pipeline commit label.
        created_by (:obj:`str`): User that created this job.
        created_on (:obj:`int`): Time at which this job was created.
        data_collector_labels (:obj:`list`): Labels of the data collectors.
        description (:obj:`str`): Job description.
        destroyer (:obj:`str`): Job destroyer.
        enable_failover (:obj:`bool`): Flag that indicates if failover is enabled.
        enable_time_series_analysis (:obj:`bool`): Flag that indicates if time series is enabled.
        execution_mode (:obj:`bool`): True for Edge and False for SDC.
        job_deleted (:obj:`bool`): Flag that indicates if this job is deleted.
        job_id (:obj:`str`): Id of the job.
        job_name (:obj:`str`): Name of the job.
        last_modified_by (:obj:`str`): User that last modified this job.
        last_modified_on (:obj:`int`): Time at which this job was last modified.
        number_of_instances (:obj:`int`): Number of instances.
        pipeline_force_stop_timeout (:obj:`int`): Timeout for Pipeline force stop.
        pipeline_id (:obj:`str`): Id of the pipeline that is running the job.
        pipeline_name (:obj:`str`): Name of the pipeline that is running the job.
        pipeline_rule_id (:obj:`str`): Rule Id of the pipeline that is running the job.
        read_policy (:py:obj:`streamsets.sdk.sch_models.ProtectionPolicy`): Read Policy of the job.
        runtime_parameters (:obj:`str`): Run-time parameters of the job.
        statistics_refresh_interval_in_millisecs (:obj:`int`): Refresh interval for statistics in milliseconds.
        status (:obj:`string`): Status of the job.
        write_policy (:py:obj:`streamsets.sdk.sch_models.ProtectionPolicy`): Write Policy of the job.
    """
    _ATTRIBUTES_TO_IGNORE = ['current_job_status', 'delete_time', 'destroyer', 'organization', 'parent_job_id',
                             'provenance_meta_data', 'runtime_parameters', 'system_job_id']
    _ATTRIBUTES_TO_REMAP = {'commit_id': 'pipelineCommitId',
                            'commit_label': 'pipelineCommitLabel',
                            'created_by': 'creator',
                            'created_on': 'createTime',
                            'data_collector_labels': 'labels',
                            'enable_failover': 'migrateOffsets',
                            'enable_time_series_analysis': 'timeSeries',
                            'execution_mode': 'edge',
                            'job_id': 'id',
                            'job_name': 'name',
                            'number_of_instances': 'numInstances',
                            'pipeline_rule_id': 'rulesId',
                            'pipeline_force_stop_timeout': 'forceStopTimeout',
                            'statistics_refresh_interval_in_millisecs': 'statsRefreshInterval'}
    _REPR_METADATA = ['job_id', 'job_name']

    # Container for details about the Data Collector running a job.
    JobDataCollector = collections.namedtuple('JobDataCollector', ['id', 'instance', 'pipeline'])

    def __init__(self, job, control_hub=None):
        super().__init__(job,
                         attributes_to_ignore=Job._ATTRIBUTES_TO_IGNORE,
                         attributes_to_remap=Job._ATTRIBUTES_TO_REMAP,
                         repr_metadata=Job._REPR_METADATA)
        self._control_hub = control_hub
        self.read_policy = None
        self.write_policy = None

    def refresh(self):
        self._data = self._control_hub.api_client.get_job(self.job_id).response.json()

    @property
    def data_collectors(self):
        data_collectors = SeekableList()
        for pipeline_status in self.pipeline_status:
            id = pipeline_status.sdc_id
            instance = self._control_hub.data_collectors.get(id=id).instance
            pipeline = instance.pipelines.get(id=pipeline_status.name.replace(':', '__'))
            data_collectors.append(Job.JobDataCollector(id=id, instance=instance, pipeline=pipeline))
        return data_collectors

    @property
    def status(self):
        # Newly added jobs have a currentJobStatus of None, so need to be handled accordingly.
        current_job_status = self._data['currentJobStatus']
        return current_job_status['status'] if current_job_status is not None else None

    @property
    def start_time(self):
        return datetime.fromtimestamp(self._data['currentJobStatus']['startTime']/1000)

    @property
    def pipeline_status(self):
        # We use type to create a trivial class as a container for the dictionaries we get from
        # SCH containing pipeline status.
        PipelineStatus = type('PipelineStatus', (BaseModel,), {})
        return SeekableList(PipelineStatus(pipeline_status, repr_metadata=['sdc_id', 'name'])
                            for pipeline_status in self._data['currentJobStatus']['pipelineStatus'])

    @property
    def runtime_parameters(self):
        return RuntimeParameters(self._data['runtimeParameters'], self)

    @runtime_parameters.setter
    def runtime_parameters(self, value):
        self._data['runtimeParameters'] = json.dumps(value)

    @property
    def acl(self):
        """Get job ACL.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ACL`.
        """
        return ACL(self._control_hub.api_client.get_job_acl(job_id=self.job_id).response.json(), self._control_hub)

    @acl.setter
    def acl(self, job_acl):
        """Update job ACL.

        Args:
            job_acl (:py:class:`streamsets.sdk.sch_models.ACL`): The job ACL instance.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        return self._control_hub.api_client.set_job_acl(job_id=self.job_id, job_acl_json=job_acl._data)


class Jobs(ModelCollection):
    """Collection of :py:class:`streamsets.sdk.sch_models.Job` instances.

    Args:
        control_hub (:py:class:`streamsets.sdk.sch.ControlHub`): Control Hub object.
    """

    def __init__(self, control_hub):
        self._control_hub = control_hub
        self._id_attr = 'job_id'

    def _get_all_results_from_api(self, id=None, organization=None, **kwargs):
        """Args order_by, order, removed, system, filter_text, job_status, job_label, edge, len, offset are not exposed
        directly as arguments because of their limited use by normal users but, could still be specified just like any
        other args with the help of kwargs.

        Args:
            id (:obj:`str`).
            organization (:obj:`str`): Organization ID.
            **kwargs: Optional other arguments to be passed to filter the results offline.

        Returns:
            A (:obj:`tuple`): of
                A :py:obj:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.Job` instances and
                A (:obj:`dict`) of local variables not used in this function.
        """
        kwargs_defaults = {'order_by': 'NAME', 'order': 'ASC', 'removed': False, 'system': False, 'filter_text': None,
                           'job_status': None, 'job_label': None, 'edge': False, 'offset': 0, 'len': -1}
        kwargs_instance = MutableKwargs(kwargs_defaults, kwargs)
        kwargs_unioned = kwargs_instance.union()
        if id is not None:
            try:
                job = self._control_hub.api_client.get_job(id).response.json()
                result = SeekableList([Job(job, self._control_hub)])
            except requests.exceptions.HTTPError:
                raise ValueError('Job (id={}) not found'.format(id))
        else:
            result = SeekableList(Job(job, self._control_hub)
                                  for job in
                                  self._control_hub.
                                  api_client.return_all_jobs(organization=organization,
                                                             order_by=kwargs_unioned['order_by'],
                                                             order=kwargs_unioned['order'],
                                                             removed=kwargs_unioned['removed'],
                                                             system=kwargs_unioned['system'],
                                                             filter_text=kwargs_unioned['filter_text'],
                                                             job_status=kwargs_unioned['job_status'],
                                                             job_label=kwargs_unioned['job_label'],
                                                             edge=kwargs_unioned['edge'],
                                                             offset=kwargs_unioned['offset'],
                                                             len=kwargs_unioned['len']
                                                             ).response.json())
        kwargs_unused = kwargs_instance.subtract()
        return result, kwargs_unused


class RuntimeParameters:
    """Wrapper for Control Hub job runtime parameters.

    Args:
        runtime_parameters (:obj:`str`): Runtime parameter.
        job (:py:obj:`streamsets.sdk.sch_models.Job`): Job object.
    """

    def __init__(self, runtime_parameters, job):
        self._data = json.loads(runtime_parameters) if runtime_parameters else {}
        self._job = job

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value
        self._propagate()

    def update(self, runtime_parameters):
        self._data.update(runtime_parameters)
        self._propagate()

    def _propagate(self):
        self._job._data['runtimeParameters'] = json.dumps(self._data)

    def __repr__(self):
        return str(self._data)

    def __bool__(self):
        return bool(self._data)


class TopologyBuilder:
    """Class with which to build instances of :py:class:`streamsets.sdk.sch_models.Topology`.

    Instead of instantiating this class directly, most users should use
        :py:meth:`streamsets.sdk.sch.ControlHub.get_topology_builder`.

    Args:
        topology (:obj:`dict`): Python object built from our Swagger TopologyJson definition.
    """

    def __init__(self, topology):
        self._topology = topology
        self._default_topology = topology

    def build(self, topology_name, description=None):
        """Build the topology.

        Args:
            topology_name (:obj:`str`): Name of the topology.
            description (:obj:`str`): Description of the topology.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Topology`.
        """
        self._topology.update({'name': topology_name,
                               'description': description})
        return Topology(topology=self._topology)


class Topology(BaseModel):
    """Model for Topology.

    Args:
        topology (:obj:`dict`): JSON representation of Topology.

    Attributes:
        commit_id (:obj:`str`): Pipeline commit id.
        commit_message (:obj:`str`): Commit Message.
        commit_time (:obj:`int`): Time at which commit was made.
        committed_by (:obj:`str`): User that made the commit.
        default_topology (:obj:`bool`): Default Topology.
        description (:obj:`str`): Topology description.
        draft (:obj:`bool`): Indicates whether this topology is a draft.
        last_modified_by (:obj:`str`): User that last modified this topology.
        last_modified_on (:obj:`int`): Time at which this topology was last modified.
        organization (:obj:`str`): Id of the organization.
        parent_version (:obj:`str`): Version of the parent topology.
        topology_definition (:obj:`str`): Definition of the topology.
        topology_id (:obj:`str`): Id of the topology.
        topology_name (:obj:`str`): Name of the topology.
        version (:obj:`str`): Version of this topology.
    """
    _ATTRIBUTES_TO_IGNORE = ['provenanceMetaData']
    _ATTRIBUTES_TO_REMAP = {'committed_by': 'committer',
                            'topology_name': 'name'}
    _REPR_METADATA = ['topology_id', 'topology_name']

    def __init__(self, topology):
        super().__init__(topology,
                         attributes_to_ignore=Topology._ATTRIBUTES_TO_IGNORE,
                         attributes_to_remap=Topology._ATTRIBUTES_TO_REMAP,
                         repr_metadata=Topology._REPR_METADATA)


class Topologies(ModelCollection):
    """Collection of :py:class:`streamsets.sdk.sch_models.Topology` instances.

    Args:
        control_hub (:py:class:`streamsets.sdk.sch.ControlHub`): An instance of the Control Hub.
    """

    def __init__(self, control_hub):
        super().__init__(control_hub)
        self._id_attr = 'topology_id'

    def _get_all_results_from_api(self, commit_id=None, organization=None, **kwargs):
        """Args offset, len_, order_by, order are not exposed directly as arguments because of their limited use by
        normal users but, could still be specified just like any other args with the help of kwargs.

        Args:
            commit_id (:obj:`str`)
            organization (:obj:`str`, optional): Default: ``None``.
            **kwargs: Optional other arguments to be passed to filter the results offline.

        Returns:
            A (:obj:`tuple`): of
                A :py:obj:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.Topology`
                instances and
                A (:obj:`dict`) of local variables not used in this function.
        """
        kwargs_defaults = {'offset': 0, 'len_': -1, 'order_by': 'NAME', 'order': 'ASC'}
        kwargs_instance = MutableKwargs(kwargs_defaults, kwargs)
        kwargs_unioned = kwargs_instance.union()
        if commit_id is not None:
            try:
                result = SeekableList(Topology(self._control_hub.api_client.get_topology_for_commit_id(commit_id=commit_id)
                                               .response.json()))
            except requests.exceptions.HTTPError:
                raise ValueError('Topology (commit_id={}) not found'.format(commit_id))
        result = SeekableList([Topology(topology)
                               for topology in
                               self._control_hub.api_client.return_all_topologies(organization=organization,
                                                                                  offset=kwargs_unioned['offset'],
                                                                                  len=kwargs_unioned['len_'],
                                                                                  order_by=kwargs_unioned['order_by'],
                                                                                  order=kwargs_unioned['order'])
                                                                                  .response.json()])
        kwargs_unused = kwargs_instance.subtract()
        return result, kwargs_unused


class ClassificationRule(UiMetadataBaseModel):
    """Classification Rule Model.

    Args:
        classification_rule (:obj:`dict`): A Python dict representation of classification rule.
        classifiers (:obj:`list`): A list of :py:class:`streamsets.sdk.sch_models.Classifier` instances.
    """
    _ATTRIBUTES_TO_IGNORE = ['classifiers']
    _ATTRIBUTES_TO_REMAP = {}

    def __init__(self, classification_rule, classifiers):
        super().__init__(classification_rule,
                         attributes_to_ignore=ClassificationRule._ATTRIBUTES_TO_IGNORE,
                         attributes_to_remap=ClassificationRule._ATTRIBUTES_TO_REMAP)
        self.classifiers = classifiers


class Classifier(UiMetadataBaseModel):
    """Classifier model.

    Args:
        classifier (:obj:`dict`): A Python dict representation of classifier.
    """
    _ATTRIBUTES_TO_IGNORE = ['patterns']
    _ATTRIBUTES_TO_REMAP = {'case_sensitive': 'sensitive',
                            'match_with': 'type',
                            'regular_expression_type': 'implementationClassValue', }

    # From https://git.io/fA0w2.
    MATCH_WITH_ENUM = {'Field Path': 'FIELD_PATH',
                       'Field Value': 'FIELD_VALUE'}

    # From https://git.io/fA0w4.
    REGULAR_EXPRESSION_TYPE_ENUM = {'RE2/J': 'RE2J_MATCHER',
                                    'Java Regular Expression': 'REGEX_MATCHER'}

    def __init__(self, classifier):
        super().__init__(classifier,
                         attributes_to_ignore=Classifier._ATTRIBUTES_TO_IGNORE,
                         attributes_to_remap=Classifier._ATTRIBUTES_TO_REMAP)

    @property
    def patterns(self):
        return [pattern['value'] for pattern in self._data['patterns']]

    @patterns.setter
    def patterns(self, values):
        self._data['patterns'] = [{'messages': [],
                                   'type': 'RSTRING',
                                   'value': value,
                                   'scrubbed': False}
                                  for value in values]

    @property
    def _id(self):
        return self._data['id']

    @_id.setter
    def _id(self, value):
        self._data['id'] = value

    @property
    def _rule_uuid(self):
        return self._data['ruleUuid']

    @_rule_uuid.setter
    def _rule_uuid(self, value):
        self._data['ruleUuid'] = value

    @property
    def _uuid(self):
        return self._data['uuid']

    @_uuid.setter
    def _uuid(self, value):
        self._data['uuid'] = value


class ClassificationRuleBuilder:
    """Class with which to build instances of :py:class:`streamsets.sdk.sch_models.ClassificationRule`.

    Instead of instantiating this class directly, most users should use
        :py:meth:`streamsets.sdk.sch.ControlHub.get_classification_rule_builder`.

    Args:
        classification_rule (:obj:`dict`): Python object defining a classification rule.
        classifier (:obj:`dict`): Python object defining a classifier.
    """

    def __init__(self, classification_rule, classifier):
        self._classification_rule = classification_rule
        self._classifier = classifier
        self.classifiers = []

    def add_classifier(self, patterns=None, match_with=None,
                       regular_expression_type='RE2/J', case_sensitive=False):
        """Add classifier to the classification rule.

        Args:
            patterns (:obj:`list`, optional): List of strings of patterns. Default: ``None``.
            match_with (:obj:`str`, optional): Default: ``None``.
            regular_expression_type (:obj:`str`, optional): Default: ``'RE2/J'``.
            case_sensitive (:obj:`bool`, optional): Default: ``False``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Classifier`.
        """
        classifier = Classifier(classifier=copy.deepcopy(self._classifier))
        classifier.patterns = patterns or ['.*']
        classifier.match_with = Classifier.MATCH_WITH_ENUM.get(match_with) or 'FIELD_PATH'
        classifier.regular_expression_type = Classifier.REGULAR_EXPRESSION_TYPE_ENUM.get(regular_expression_type)
        classifier.case_sensitive = case_sensitive

        classifier._uuid = str(uuid.uuid4())
        classifier._id = '{}:1'.format(classifier._uuid)
        classifier._rule_uuid = self._classification_rule['uuid']
        self.classifiers.append(classifier)
        return classifier

    def build(self, name, category, score):
        """Build the classification rule.

        Args:
            name (:obj:`str`): Classification Rule name.
            category (:obj:`str`): Classification Rule category.
            score (:obj:`float`): Classification Rule score.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ClassificationRule`.
        """
        classification_rule = ClassificationRule(classification_rule=self._classification_rule,
                                                 classifiers=self.classifiers)
        classification_rule.name = name
        classification_rule.category = category
        classification_rule.score = score
        return classification_rule


class ProtectionPolicy(UiMetadataBaseModel):
    """Model for Protection Policy.

    Args:
        protection_policy (:obj:`dict`): JSON representation of Protection Policy.
        procedures (:obj:`list`): A list of :py:class:`streamsets.sdk.sch_models.PolicyProcedure` instances,
                    Default: ``None``.
    """
    _ATTRIBUTES_TO_IGNORE = ['enactment', 'procedures']
    _ATTRIBUTES_TO_REMAP = {}
    _REPR_METADATA = ['name', 'enactment']

    ENACTMENT_ENUM = {'Read': 'READ',
                      'Write': 'WRITE'}

    def __init__(self, protection_policy, procedures=None):
        super().__init__(protection_policy,
                         attributes_to_ignore=ProtectionPolicy._ATTRIBUTES_TO_IGNORE,
                         attributes_to_remap=ProtectionPolicy._ATTRIBUTES_TO_REMAP,
                         repr_metadata=ProtectionPolicy._REPR_METADATA)
        self.procedures = procedures

    @property
    def _id(self):
        return self._data['id']

    @_id.setter
    def _id(self, value):
        self._data['id'] = value

    @property
    def enactment(self):
        return next(k
                    for k, v in ProtectionPolicy.ENACTMENT_ENUM.items()
                    if v == self._data['enactment']['value'])

    @enactment.setter
    def enactment(self, value):
        self._data['enactment']['value'] = value


class ProtectionPolicies(ModelCollection):
    """Collection of :py:class:`streamsets.sdk.sch_models.ProtectionPolicy` instances."""

    def _get_all_results_from_api(self, **kwargs):
        """
        Args:
            **kwargs: Optional other arguments to be passed to filter the results offline.

        Returns:
            A (:obj:`tuple`): of
                A :py:obj:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.ProtectionPolicy`
                instances and
                A (:obj:`dict`) of local variables not used in this function.
        """
        protection_policies = []
        response = self._control_hub.api_client.get_protection_policy_list().response.json()['response']
        for protection_policy in response:
            protection_policy['data'].pop('messages', None)
            protection_policies.append(ProtectionPolicy(protection_policy['data']))
        return SeekableList(protection_policies), kwargs


class ProtectionPolicyBuilder:
    """Class with which to build instances of :py:class:`streamsets.sdk.sch_models.ProtectionPolicy`.

    Instead of instantiating this class directly, most users should use
        :py:meth:`streamsets.sdk.sch.ControlHub.get_protection_policy_builder`.

    Args:
        protection_policy (:obj:`dict`): Python object defining a protection policy.
        policy_procedure (:obj:`dict`): Python object defining a policy procedure.
    """

    def __init__(self, protection_policy, policy_procedure):
        self._protection_policy = protection_policy
        self._policy_procedure = policy_procedure
        self.procedures = []

    def add_procedure(self, classification_score_threshold=0.5, procedure_basis='Category Pattern',
                      classification_category_pattern=None, field_path=None, protection_method=None):
        procedure = PolicyProcedure(policy_procedure=copy.deepcopy(self._policy_procedure))
        procedure.classification_score_threshold = classification_score_threshold
        procedure.procedure_basis = PolicyProcedure.PROCEDURE_BASIS_ENUM.get(procedure_basis)
        if procedure_basis == 'Category Pattern':
            procedure.classification_category_pattern = classification_category_pattern
        elif procedure_basis == 'Field Path':
            procedure.field_path = field_path
        # https://git.io/fAE0K
        procedure.protection_method = json.dumps({'issues': None,
                                                  'schemaVersion': 1,
                                                  'stageConfiguration': protection_method._data})

        self.procedures.append(procedure)

    def build(self, name, enactment):
        protection_policy = ProtectionPolicy(self._protection_policy, self.procedures)
        protection_policy.name = name
        protection_policy.enactment = ProtectionPolicy.ENACTMENT_ENUM.get(enactment)

        return protection_policy


class PolicyProcedure(UiMetadataBaseModel):
    """Model for Policy Procedure.

    Args:
        policy_procedure (:obj:`dict`): JSON representation of Policy Procedure.
    """
    PROCEDURE_BASIS_ENUM = {'Category Pattern': 'CATEGORY_PATTERN',
                            'Field Path': 'FIELD_PATH'}

    _ATTRIBUTES_TO_IGNORE = ['id', 'optimisticLockVersion', 'version']
    _ATTRIBUTES_TO_REMAP = {'classification_category_pattern': 'classificationCategory',
                            'classification_score_threshold': 'threshold',
                            'procedure_basis': 'subjectType',
                            'protection_method': 'transformerConfig'}

    def __init__(self, policy_procedure):
        super().__init__(policy_procedure,
                         attributes_to_ignore=PolicyProcedure._ATTRIBUTES_TO_IGNORE,
                         attributes_to_remap=PolicyProcedure._ATTRIBUTES_TO_REMAP)

    @property
    def _id(self):
        return self._data['id']

    @_id.setter
    def _id(self, value):
        self._data['id'] = value

    @property
    def _policy_id(self):
        return self._data['policyId']

    @_policy_id.setter
    def _policy_id(self, value):
        self._data['policyId'] = value


class ProtectionMethod(Stage):
    """Protection Method Model.

    Args:
        stage (:obj:`dict`): JSON representation of a stage.
    """
    STAGE_LIBRARY = 'streamsets-datacollector-dataprotector-lib'

    def __init__(self, stage):
        super().__init__(stage, label=stage['uiInfo']['label'])


class ProtectionMethodBuilder:
    """Class with which to build instances of :py:class:`streamsets.sdk.sch_models.ProtectionMethod`.

    Instead of instantiating this class directly, most users should use
        :py:meth:`streamsets.sdk.sch.ControlHub.get_protection_method_builder`.

    Args:
        pipeline_builder (:py:class:`streamsets.sdk.sch_models.PipelineBuilder`): Pipeline Builder object.
    """

    def __init__(self, pipeline_builder):
        self._pipeline_builder = pipeline_builder

    def build(self, method):
        method_stage = self._pipeline_builder.add_stage(
            label=method, library=ProtectionMethod.STAGE_LIBRARY)
        # We generate a single output lane to conform to SDP's expectations for detached stages.
        method_stage.add_output()
        protection_method = type(method_stage.stage_name,
                                 (ProtectionMethod,),
                                 {'_attributes': method_stage._attributes})
        return protection_method(method_stage._data)


class ReportDefinition(BaseModel):
    """Model for Report Definition.

    Args:
        report_def (:obj:`dict`): JSON representation of Report Definition.
    """
    _REPR_METADATA = ['id', 'name']

    def __init__(self, report_def):
        super().__init__(report_def, repr_metadata=ReportDefinition._REPR_METADATA)


class Report(BaseModel):
    """Model for Report.

    Args:
        report (:obj:`dict`): JSON representation of Report.
    """
    _REPR_METADATA = ['id', 'name']

    def __init__(self, report):
        super().__init__(report, repr_metadata=Report._REPR_METADATA)


class ScheduledTaskBaseModel(BaseModel):
    """Base Model for Scheduled Task related classes."""

    def __getattr__(self, name):
        name_ = python_to_json_style(name)
        if name in self._attributes_to_remap:
            remapped_name = self._attributes_to_remap[name]
            return (self._data[remapped_name]['value']
                   if 'value' in self._data[remapped_name] else self._data[remapped_name])
        elif (name_ in self._data and
              name not in self._attributes_to_ignore and
              name not in self._attributes_to_remap.values()):
            return self._data[name_]['value'] if 'value' in self._data[name_] else self._data[name_]
        raise AttributeError('Could not find attribute {}.'.format(name_))

    def __setattr__(self, name, value):
        name_ = python_to_json_style(name)
        if name in self._attributes_to_remap:
            remapped_name = self._attributes_to_remap[name]
            if 'value' in self._data[remapped_name]:
                self._data[remapped_name]['value'] = value
            else:
                self._data[remapped_name] = value
        elif (name_ in self._data and
              name not in self._attributes_to_ignore and
              name not in self._attributes_to_remap.values()):
            if 'value' in self._data[name_]:
                self._data[name_]['value'] = value
            else:
                self._data[name_] = value
        else:
            super().__setattr__(name, value)


class ScheduledTaskBuilder:
    """Builder for Scheduled Task.

    Instead of instantiating this class directly, most users should use
        :py:meth:`streamsets.sdk.sch.ControlHub.get_scheduled_task_builder`.

    Args:
        job_selection_types (:py:obj:`dict`): JSON representation of job selection types.
        control_hub (:py:class:`streamsets.sdk.ControlHub`): Control Hub instance.
    """

    def __init__(self, job_selection_types, control_hub):
        self._job_selection_types = job_selection_types
        self._control_hub = control_hub

    def build(self, job, action='START', name=None, description=None, crontab_mask="0 0 1/1 * ? *", time_zone="UTC",
              status="RUNNING", start_time=None, end_time=None, missed_trigger_handling='IGNORE'):
        """Builder for Scheduled Task.

        Args:
            job (:py:class:`streamsets.sdk.sch_models.Job`): Job object.
            action (:obj:`str`, optional): One of the {'START', 'STOP', 'UPGRADE'} actions. Default: ``START``.
            name (:obj:`str`, optional): Name of the task. Default: ``None``.
            description (:obj:`str`, optional): Description of the task. Default: ``None``.
            crontab_mask (:obj:`str`, optional): Schedule in cron syntax. Default: ``"0 0 1/1 * ? *"``. (Daily at 12).
            time_zone (:obj:`str`, optional): Time zone. Default: ``"UTC"``.
            status (:obj:`str`, optional): One of the {'RUNNING', 'PAUSED'} statuses. Default: ``RUNNING``.
            start_time (:obj:`str`, optional): Start time of task. Default: ``None``.
            end_time (:obj:`str`, optional): End time of task. Default: ``None``.
            missed_trigger_handling (:obj:`str`, optional): One of {'IGNORE', 'RUN ALL', 'RUN ONCE'}.
                                                            Default: ``IGNORE``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ScheduledTask`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'job', 'action'))

        self._job_selection_types['jobId']['value'] = job.job_id
        self._job_selection_types['jobName']['value'] = job.job_name
        _response = self._control_hub.api_client.trigger_selection_info(data={'data': self._job_selection_types},
                                                                        api_version=2)
        task = _response.response.json()['response']['data']

        for key, value in params.items():
            task[key]['value'] = value

        return ScheduledTask(task, self._control_hub)


class ScheduledTask(ScheduledTaskBaseModel):
    """Model for Scheduled Task.

    Args:
        task (:py:obj:`dict`): JSON representation of task.
        control_hub (:py:class:`streamsets.sdk.ControlHub`): Control Hub instance.
    """
    _REPR_METADATA = ['id', 'name', 'status']

    def __init__(self, task, control_hub=None):
        super().__init__(task,
                         repr_metadata=ScheduledTask._REPR_METADATA)
        self._control_hub = control_hub
        self._allowed_actions = {'PAUSE', 'RESUME', 'KILL', 'DELETE'}
        # With this we would be able to call actions like task.pause(), task.kill(), task.resume() and task.delete()
        for action in self._allowed_actions:
            setattr(self, action.lower(), partial(self._perform_action, action=action))

    @property
    def runs(self):
        """Get Scheduled Task Runs.

        Returns:
            A :py:obj:`streamsets.sdk.utils.SeekableList` of inherited instances of
            :py:class:`streamsets.sdk.sch_models.ScheduledTaskRun`.
        """
        _repsonse = self._control_hub.api_client.get_scheduled_task(id=self.id,
                                                                    run_info=True,
                                                                    audit_info=False,
                                                                    api_version=2)
        runs = _repsonse.response.json()['response']['data']['runs']
        return SeekableList(ScheduledTaskRun(run) for run in runs)

    @property
    def audits(self):
        """Get Scheduled Task Audits.

        Returns:
            A :py:obj:`streamsets.sdk.utils.SeekableList` of inherited instances of
            :py:class:`streamsets.sdk.sch_models.ScheduledTaskAudit`.
        """
        _response = self._control_hub.api_client.get_scheduled_task(id=self.id,
                                                                    run_info=False,
                                                                    audit_info=True,
                                                                    api_version=2)
        audits = _response.response.json()['response']['data']['audits']
        return SeekableList(ScheduledTaskAudit(audit) for audit in audits)

    def _perform_action(self, action):
        """Perform a specified action on this scheduled task.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ScheduledTask`.
        """
        assert action in self._allowed_actions
        response = self._control_hub.api_client.perform_action_on_scheduled_task(self.id,
                                                                                 action,
                                                                                 api_version=2).response.json()
        updated_task = response['response']['data']
        self._data = updated_task
        return self


class ScheduledTasks(ModelCollection):
    """Collection of :py:class:`streamsets.sdk.sch_models.ScheduledTask` instances."""

    def _get_all_results_from_api(self, **kwargs):
        """Args order_by, offset, len are not exposed directly as arguments because of their limited use by normal
        users but, could still be specified just like any other args with the help of kwargs.

        Args:
            **kwargs: Optional other arguments to be passed to filter the results.

        Returns:
            A (:obj:`tuple`): of
                A :py:obj:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.SchedulerTask`
                instances and
                A (:py:obj:`dict`) of local variables not used in this function.
        """
        kwargs_defaults = {'offset': None, 'len': None, 'order_by': None}
        kwargs_instance = MutableKwargs(kwargs_defaults, kwargs)
        kwargs_unioned = kwargs_instance.union()
        tasks = self._control_hub.api_client.get_scheduled_tasks(kwargs_unioned['order_by'],
                                                                 kwargs_unioned['offset'],
                                                                 kwargs_unioned['len'],
                                                                 api_version=2).response.json()['response']
        result = SeekableList(ScheduledTask(task['data'], self._control_hub) for task in tasks)
        kwargs_unused = kwargs_instance.subtract()
        return result, kwargs_unused


class ScheduledTaskRun(ScheduledTaskBaseModel):
    """Scheduled Task Run.

    Args:
        run (:py:obj:`dict`): JSON representation if scheduled task run.
    """
    _REPR_METADATA = ['id', 'scheduledTime']

    def __init__(self, run):
        super().__init__(run,
                         repr_metadata=ScheduledTaskRun._REPR_METADATA)


class ScheduledTaskAudit(ScheduledTaskBaseModel):
    """Scheduled Task Audit.

    Args:
        run (:py:obj:`dict`): JSON representation if scheduled task audit.
    """
    _REPR_METADATA = ['id', 'action']

    def __init__(self, audit):
        super().__init__(audit,
                         repr_metadata=ScheduledTaskAudit._REPR_METADATA)
