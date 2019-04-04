from cloudshell.helpers.scripts.cloudshell_dev_helpers import attach_to_cloudshell_as
import cloudshell.helpers.scripts.cloudshell_scripts_helpers as sh
import cloudshell.api.cloudshell_api as api

res_id = 'f6dea0aa-4fb8-424e-b69d-8e5e2f14358b'

attach_to_cloudshell_as(
    user='admin',
    password='admin',
    domain='Global',
    reservation_id=res_id,
    server_address='localhost'
)
session = sh.get_api_session()

pass

