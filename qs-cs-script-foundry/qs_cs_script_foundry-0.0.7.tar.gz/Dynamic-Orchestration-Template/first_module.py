from cloudshell.workflow.orchestration.sandbox import Sandbox
from helper_code.custom_helpers import sb_print, get_reservation_resources
import cloudshell.helpers.scripts.cloudshell_scripts_helpers as script_help


# ========== Primary Function ==========
def first_module_flow(sandbox, components=None):
    """
    Function passed to orchestration flow MUST have two parameters
    :param Sandbox sandbox:
    :param components
    :return:
    """
    resources = get_reservation_resources(sandbox)
    resource_count = len(resources)
    sb_print(sandbox, "resources in sandbox: " + str(resource_count))

    # Get Resource Details sample snippet
    """
    res_details = script_help.get_resource_context_details()
    sb_print(sandbox, "resource name is: " + res_details.name)
    """


