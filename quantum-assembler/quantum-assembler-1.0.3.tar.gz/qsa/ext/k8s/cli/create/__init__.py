"""Create Kubernetes resources."""
from qsa.lib.cli import Command
from .certificate import CreateCertificateCommand
from .clusterissuer import CreateClusterIssuerCommand
from .dmz import CreateDemilitarizedZoneCommand
from .ns import CreateNamespaceCommand
from .pairednetworkpolicy import CreatePairNetworkPolicyCommand
from .pki import CreatePublicKeyInfrastructureCommand
from .serviceaccount import CreateServiceAccountCommand
from .nginx_ingress import CreateIngressNginxCommand


class CreateCommand(Command):
    command_name = 'create'
    subcommands = [
        CreateNamespaceCommand,
        CreateServiceAccountCommand,
        CreatePublicKeyInfrastructureCommand,
        CreateIngressNginxCommand,
        CreateDemilitarizedZoneCommand,
        CreateClusterIssuerCommand,
        CreateCertificateCommand,
        CreatePairNetworkPolicyCommand
    ]
    help_text = (
        "Specify the resource to create. For a list of valid resource names, "
        "run qsa k8s create --help"
    )
