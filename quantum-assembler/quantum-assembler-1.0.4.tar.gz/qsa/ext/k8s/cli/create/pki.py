"""Ensure that ``cert-manager`` and cluster issuers are
configured.
"""
import ioc

from qsa.lib.cli import Command
from qsa.lib.cli import Enable
from qsa.ext.k8s.const import TAG_DEPLOYMENT_PHASE
from qsa.ext.k8s.services import ResourceCreateService
from qsa.ext.k8s.tasks import KubernetesNamespaceTask


NAMESPACE = 'cert-manager'
APP_NAME = 'cert-manager'
APP_MANIFEST = "https://raw.githubusercontent.com/jetstack/cert-manager/release-0.7/deploy/manifests/cert-manager-no-webhook.yaml"


class CreatePublicKeyInfrastructureCommand(Command):
    command_name = 'pki'
    help_text = __doc__
    args = [
        Enable('--disable-webhook')
    ]
    codebase = ioc.class_property('core:CodeRepository')

    def handle(self, quantum, project, codebase, ansible, args, deployment):
        """Create a namespace to hold the ``cert-manager`` deployment
        and the custom resource definitions.
        """
        service = ResourceCreateService(quantum, project, ansible, codebase,
            deployment)
        try:
            with self.codebase.commit("Initialize PKI", noprefix=True):
                service.importmanifest(APP_MANIFEST,
                    name="installed cert-manager ({kind})",
                    part_of='cert-manager', force_playbook='bootstrap',
                    tags=[f"{TAG_DEPLOYMENT_PHASE}:bootstrap"])

                # Persist the history
                quantum.persist()
        except service.NamespaceExists:
            self.fail("PKI already deployed.")
