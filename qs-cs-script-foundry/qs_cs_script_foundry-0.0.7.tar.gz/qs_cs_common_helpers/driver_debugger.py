from cloudshell.shell.core.driver_context import InitCommandContext, ResourceCommandContext

from cloudshell.helpers.scripts.cloudshell_dev_helpers import attach_to_cloudshell_as
import cloudshell.helpers.scripts.cloudshell_scripts_helpers as sh

class driver_debugger():
    def __init__(self, credentials, reservation_id ,resource_name=None, service_name=None):
        if resource_name:
            attach_to_cloudshell_as(user=credentials["user"],
                                    password=credentials["password"],
                                    domain=credentials["domain"],
                                    reservation_id=reservation_id,
                                    server_address=credentials["server"],
                                    resource_name=resource_name)
        elif service_name:
            attach_to_cloudshell_as(user=credentials["user"],
                                    password=credentials["password"],
                                    domain=credentials["domain"],
                                    reservation_id=reservation_id,
                                    server_address=credentials["server"],
                                    resource_name=resource_name)
        else:
            attach_to_cloudshell_as(user=credentials["user"],
                                    password=credentials["password"],
                                    domain=credentials["domain"],
                                    reservation_id=reservation_id,
                                    server_address=credentials["server"],
                                    resource_name=resource_name)


    def get_driver_debugger(self):
        session = sh.get_api_session()
        token = session.token_id

        reservation_context = sh.get_reservation_context_details()
        reservation_context.reservation_id = reservation_context.id

        connectivity_context = sh.get_connectivity_context_details()
        connectivity_context.admin_auth_token = token

        self.resource_command_context = ResourceCommandContext(
            connectivity=connectivity_context,
            resource=sh.get_resource_context_details(),
            reservation=reservation_context,
            connectors=''
        )

        self.init_context = InitCommandContext(
            connectivity=sh.get_connectivity_context_details(),
            resource=sh.get_resource_context_details()
        )


