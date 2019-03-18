from parse_config import parse_commands
from cloudshell.api.cloudshell_api import CloudShellAPISession, InputNameValue
import cloudshell.helpers.scripts.cloudshell_scripts_helpers as sh
from cloudshell.helpers.scripts.cloudshell_dev_helpers import attach_to_cloudshell_as
from cloudshell.core.logger import qs_logger


res_id = '45d59999-8f95-4adc-b196-c3cf7d8fceba'

attach_to_cloudshell_as(
    user='yoav.e',
    password='1234',
    domain='Global',
    reservation_id=res_id,
    server_address='40.91.201.107'
)
session = sh.get_api_session()


logger = qs_logger.get_qs_logger(
        log_group=res_id,
        log_category='a',
        log_file_prefix='a'
    )

command_parser = parse_commands(session=session, res_id=res_id, logger=logger)

reservation_description = session.GetReservationDetails(res_id).ReservationDescription
parsed_commands = command_parser.replace_placeholders('skybox_server', 'txt', reservation_description)

pass