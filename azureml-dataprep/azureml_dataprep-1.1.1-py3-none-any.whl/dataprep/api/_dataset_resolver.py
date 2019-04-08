import json
from .engineapi.enginerequests import get_requests_channel


def _resolve_dataset(request, writer):
    from azureml.core import Workspace
    from azureml.contrib.dataset import Dataset

    ws_name = request.get('ws_name')
    subscription = request.get('subscription')
    resource_group = request.get('resource_group')
    if not ws_name or not subscription or not resource_group:
        writer.write(json.dumps({'result': 'error', 'error': 'InvalidWorkspace'}))
        return

    try:
        ws = Workspace.get(ws_name, subscription_id=subscription, resource_group=resource_group)
        dataset_name = request.get('dataset_name')
        dataset_version = request.get('dataset_version')
        definition = Dataset._get_definition_json(ws, dataset_name, dataset_version)
        writer.write(json.dumps({'result': 'success', 'data': definition}))
    except Exception as e:
        writer.write(json.dumps({'result': 'error', 'error': str(e)}))


def register_dataset_resolver():
    get_requests_channel().register_handler('resolve_dataset', _resolve_dataset)
