'''
users
======

The following methods allow for interaction into the Tenable.sc 
`User <>`_ API.  These 
items are typically seen under the **Users** section of Tenable.sc.

Methods available on ``sc.users``:

.. rst-class:: hide-signature
.. autoclass:: UserAPI

    .. automethod:: create
    .. automethod:: delete
    .. automethod:: details
    .. automethod:: edit
    .. automethod:: list
'''
from .base import SCEndpoint

class UserAPI(SCEndpoint):
    def _constructor(self, **kw):
        '''
        Handles parsing the keywords and returns a user definition document
        '''
        if 'role' in kw:
            # Validate role as int and pass to roleID
            kw['roleID'] = self._check('role', kw['role'], int)
            del(kw['role'])

        if 'group' in kw:
            # Validate group asd int and pass to groupID
            kw['groupID'] = self._check('group', kw['group'], int)
            del(kw['group'])
        
        if 'org' in kw:
            # Validate org as int and pass to orgID
            kw['orgID'] = self._check('org', kw['org'], int)
        
        if 'responsibility':
            # Validate responsibility as an int and pass to responsibleAssetID
            kw['responsibleAssetID'] = self._check(
                'responsibility', kw['responsibility'], int)
            del(kw['responsibility'])
        
        # all of the following keys are string values and do not require any
        # case conversion.  We will simply iterate through them and verify that
        # they are in-fact strings.
        keys = [
            'ldapUsername', 'username', 'firstname', 'lastname', 'title', 
            'email', 'address', 'city', 'state', 'country', 'phone', 'fax', 
            'fingerprint', 'status'
        ]
        for k in keys:
            if k in kw:
                self._check(k, kw[k], str)
        
        if 'is_locked' in kw:
            # Convert the is_locked keyword from a boolean value into a string
            # interpretation of that value.
            kw['locked'] = str(self._check(
                'is_locked', kw['is_locked'], bool)).lower()
            del(kw['is_locked'])
        
        if 'auth_type' in kw:
            # Verify that auth_type is one of the correct possible values and
            # store it within the camelCased version of the parameter.
            kw['authType'] = self._check('auth_type', kw['auth_type'], str,
                choices=['ldap', 'legacy', 'saml', 'tns'])
            del(kw['authType'])
        
        if 'email_notice' in kw:
            # Verify that email_notice is one of the correct possible values and
            # store it within the camelCased version of the parameter.
            kw['emailNotice'] = self._check(
                'email_notice', kw['email_notice'], str, choices=[
                    'both', 'id', 'none', 'password'])
        
        if 'timezone' in kw:
            # Convert the timezone parameter into the preference dictionary
            # item thats expected by the API.
            kw['preferences'] = [{
                'name': 'timezone',
                'tag': 'system',
                'value': self._check('timezone', kw['timezone'], str)
            }]
        
        if 'update_password' in kw:
            # Convert the update_password keyword from a boolean value into a 
            # string interpretation of that value.
            kw['mustChangePassword'] = str(self._check(
                'update_password', kw['update_password'], bool)).lower()
        
        if 'managed_usergroups' in kw:
            # Convert the managed_groups list into a listing of dictionaries
            # with an id parameter.
            kw['managedUsersGroups'] = [{'id': self._check('group:id', i, int)}
                for i in self._check(
                    'managed_usergroups', kw['managed_usergroups'], list)]
            del(kw['managed_usergroups'])
        
        if 'managed_userobjs' in kw:
            # Convert the managed_groups list into a listing of dictionaries
            # with an id parameter.
            kw['managedObjectsGroups'] = [{'id': self._check('group:id', i, int)}
                for i in self._check(
                    'managed_userobjs', kw['managed_userobjs'], list)]
            del(kw['managed_userobjs'])
        
        if 'def_reports' in kw:
            # Should the default user reports be built as part of the user
            # creation?
            kw['importReports'] = str(self._check(
                'def_reports', kw['def_reports'], bool)).lower()
            del(kw['def_reports'])
        
        if 'def_dashboards' in kw:
            # Should the default user dashboards be built as part of the user
            # creation?
            kw['importDashboards'] = str(self._check(
                'def_dashboards', kw['def_dashboards'], bool)).lower()
            del(kw['def_dashboards'])

        if 'def_reportcards' in kw:
            # Should the default user dashboards be built as part of the user
            # creation?
            kw['importARCs'] = str(self._check(
                'def_reportcards', kw['def_reportcards'], bool)).lower()
            del(kw['def_reportcards'])
        
        return kw
    
    def create(self, username, password, role, **kw):
        '''
        Creates a user.

        + `user: create <>`_

        Args:
            username (str): 
                The username for the account
            password (str):
                The password for the user to create
            role (int):
                The role that should be assigned to this user.
            address (str, optional):
                Optional street address information to associate to the user.
            auth_type (str, optional):
                The Authentication type to use for the user.
            
            

        
        Returns:
            dict: The newly created user. 
        
        Examples:
            >>> user = sc.users.create()
        '''
        kw['username'] = name
        kw['auth_type'] = kw.get('auth_type', 'tns')
        payload = self._constructor(**kw)
        return self._api.post('user', json=payload).json()['response']
    
    def details(self, id, fields=None):
        '''
        Returns the details for a specific user.

        + `user: details <>`_

        Args:
            id (int): The identifier for the user.
            fields (list, optional): A list of attributes to return.

        Returns:
            dict: The user resource record.

        Examples:
            >>> user = sc.users.details(1)
            >>> pprint(user)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str) for f in fields])

        return self._api.get('user/{}'.format(self._check('id', id, int)),
            params=params).json()['response']
    
    def edit(self, id, **kw):
        '''
        Edits a user.

        + `user: edit <>`_

        Args:
        
        
        Returns:
            dict: The newly updated user. 
        
        Examples:
            >>>user = sc.users.edit()
        '''
        payload = self._constructor(**kw)
        return self._api.patch('user', json=payload).json()['response']

    def delete(self, id):
        '''
        Removes a user.

        + `user: delete <>`_

        Args:
            id (int): The numeric identifier for the user to remove.
        
        Returns:
            str: An empty response.
        
        Examples:
            >>> sc.users.delete(1)
        '''
        return self._api.delete('user/{}'.format(
            self._check('id', id, int))).json()['response']
    
    def list(self, fields=None):
        '''
        Retrieves the list of scan zone definitions.

        + `user: list <>`_

        Args:
            fields (list, optional): 
                A list of attributes to return for each user.

        Returns:
            list: A list of scan zone resources.

        Examples:
            >>> for user in sc.users.list():
            ...     pprint(user)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str) 
                for f in fields])
        
        return self._api.get('user', params=params).json()['response']
