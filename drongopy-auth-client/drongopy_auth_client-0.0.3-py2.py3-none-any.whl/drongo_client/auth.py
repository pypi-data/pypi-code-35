from drongo.client import DrongoClient


class AuthClient(DrongoClient):
    def user_from_token(self, token):
        response = self.get(
            '/users/from-token',
            params={'token': token})
        if response['status'] == 'ERROR':
            return False, None
        else:
            return True, response['payload']

    def user_create(self, username, password):
        login_data = {'username': username, 'password': password}
        response = self.post_json('/users', login_data)
        if response['status'] == 'OK':
            return True, response['payload']
        else:
            return False, response['errors']

    def user_verify_credentials(self, username, password):
        login_data = {'username': username, 'password': password}
        response = self.post_json(
            '/users/operations/verify-credentials', login_data)
        if response['status'] == 'OK':
            return True, response['payload']
        else:
            return False, response['errors']

    def user_token_create(self, username):
        url = '/users/{username}/operations/token-create'.format(
            username=username
        )
        response = self.post_json(url, {})
        if response['status'] == 'OK':
            return True, response['payload']
        else:
            return False, response['errors']

    def user_token_delete(self, token):
        url = '/users/operations/token-delete'
        response = self.delete(url, params={'token': token})
        if response['status'] == 'OK':
            return True, response['payload']
        else:
            return False, response['errors']

    def user_token_refresh(self, token):
        pass  # FIXME: Implement

    def user_login(self, username, password):
        status, _ = self.user_verify_credentials(username, password)
        if status:
            status, token = self.user_token_create(username)
            if status:
                return True, token
        return False, None

    def user_change_password(self, username, password):
        login_data = {'username': username, 'password': password}
        response = self.post_json(
            '/users/operations/change-password', login_data)
        if response['status'] == 'OK':
            return True, response['payload']
        else:
            return False, response['errors']

    def user_logout(self, token):
        self.user_token_delete(token)

    def user_activate(self, username):
        response = self.post_json(
            '/users/{username}/operations/activate'.format(
                username=username), {}
        )
        if response['status'] == 'OK':
            return True, response['payload']
        else:
            return False, response['errors']

    def user_deactivate(self, username):
        response = self.post_json(
            '/users/{username}/operations/deactivate'.format(
                username=username), {}
        )
        if response['status'] == 'OK':
            return True, response['payload']
        else:
            return False, response['errors']

    def user_list(self, active_only=True, page_number=1, page_size=50):
        response = self.get('/users')
        if response['status'] == 'OK':
            return True, response['payload']
        else:
            return False, response['errors']

    def group_create(self, groupname):
        response = self.post_json('/groups', {'name': groupname})
        if response['status'] == 'OK':
            return True, response['payload']
        else:
            return False, response['errors']

    def group_delete(self, groupname):
        response = self.delete(
            '/groups/{groupname}'.format(groupname=groupname))
        if response['status'] == 'OK':
            return True, response['payload']
        else:
            return False, response['errors']

    def group_list(self, page_number=1, page_size=50):
        response = self.get(
            '/groups',
            {'page_number': page_number, 'page_size': page_size})
        if response['status'] == 'OK':
            return True, response['payload']
        else:
            return False, response['errors']

    def group_add_user(self, groupname, username):
        response = self.post_json(
            '/groups/{groupname}/users'.format(
                groupname=groupname
            ),
            {'username': username}
        )
        if response['status'] == 'OK':
            return True, response['payload']
        else:
            return False, response['errors']

    def group_delete_user(self, groupname, username):
        response = self.delete(
            '/groups/{groupname}/users/{username}'.format(
                groupname=groupname, username=username))
        if response['status'] == 'OK':
            return True, response['payload']
        else:
            return False, response['errors']

    def group_list_users(self, groupname):
        response = self.get(
            '/groups/{groupname}/users'.format(groupname=groupname))
        if response['status'] == 'OK':
            return True, response['payload']
        else:
            return False, response['errors']

    def user_list_groups(self, username):
        response = self.get(
            '/users/{username}/groups'.format(username=username))
        if response['status'] == 'OK':
            return True, response['payload']
        else:
            return False, response['errors']

    def permission_add_client(self, permission_id, client):
        response = self.post_json(
            '/permissions/{permission_id}/clients'.format(
                permission_id=permission_id),
            {'client': client})
        if response['status'] == 'OK':
            return True, response['payload']
        else:
            return False, response['errors']

    def permission_delete_client(self, permission_id, client):
        response = self.delete(
            '/permissions/{permission_id}/clients/{client}'.format(
                permission_id=permission_id,
                client=client))
        if response['status'] == 'OK':
            return True, response['payload']
        else:
            return False, response['errors']

    def permission_list_clients(self, permission_id):
        response = self.get(
            '/permissions/{permission_id}/clients'.format(
                permission_id=permission_id))
        if response['status'] == 'OK':
            return True, response['payload']
        else:
            return False, response['errors']

    def permission_check_user(self, permission_id, username):
        response = self.post_json(
            '/permissions/{permission_id}/check-user'.format(
                permission_id=permission_id),
            {'username': username})
        if response['status'] == 'OK':
            return True, response['payload']
        else:
            return False, response['errors']

    def object_permission_add_client(
            self, object_type, object_id, permission_id, client):
        response = self.post_json(
            (
                '/permissions/{permission_id}/objects/'
                '{object_type}/{object_id}/clients'
            ).format(
                permission_id=permission_id,
                object_type=object_type,
                object_id=object_id),
            {'client': client}
        )
        if response['status'] == 'OK':
            return True, response['payload']
        else:
            return False, response['errors']

    def object_permission_delete_client(
            self, object_type, object_id, permission_id, client):
        response = self.delete(
            (
                '/permissions/{permission_id}/objects/'
                '{object_type}/{object_id}/clients/{client}'
            ).format(
                permission_id=permission_id,
                object_type=object_type,
                object_id=object_id,
                client=client))
        if response['status'] == 'OK':
            return True, response['payload']
        else:
            return False, response['errors']

    def object_permission_list_clients(
            self, object_type, object_id, permission_id):
        response = self.get(
            (
                '/permissions/{permission_id}/objects/'
                '{object_type}/{object_id}/clients'
            ).format(
                permission_id=permission_id,
                object_type=object_type,
                object_id=object_id))
        if response['status'] == 'OK':
            return True, response['payload']
        else:
            return False, response['errors']

    def object_permission_check_user(
            self, object_type, object_id, permission_id, username):
        response = self.post_json(
            (
                '/permissions/{permission_id}/objects/'
                '{object_type}/{object_id}/check-user'
            ).format(
                permission_id=permission_id,
                object_type=object_type,
                object_id=object_id),
            {'username': username})
        if response['status'] == 'OK':
            return True, response['payload']
        else:
            return False, response['errors']

    def object_owner_set(self, object_type, object_id, username):
        response = self.put_json(
            '/objects/{object_type}/{object_id}/operations/set-owner'.format(
                object_type=object_type,
                object_id=object_id),
            {'username': username})
        if response['status'] == 'OK':
            return True, response['payload']
        else:
            return False, response['errors']

    def object_owner_get(self, object_type, object_id):
        response = self.get(
            '/objects/{object_type}/{object_id}/owner'.format(
                object_type=object_type,
                object_id=object_id))
        if response['status'] == 'OK':
            return True, response['payload']
        else:
            return False, response['errors']
