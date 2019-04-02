"""Create a new ``ServiceAccount`` in a Kubernetes cluster in the
specified namespace."""
from qsa.lib.cli import Command
from qsa.lib.cli import Argument
from qsa.lib.cli import Enable
from qsa.lib.cli import ArgumentList
from qsa.ext.k8s.tasks import KubernetesServiceAccountTask


class CreateServiceAccountCommand(Command):
    command_name = 'serviceaccount'
    help_text = __doc__
    args = [
        Argument('namespace',
            help="a DNS-1123 compliant symbolic name identifying the Namespace."),
        Argument('name',
            help="specify the name of the service account."),
        Enable('--automount',
            help="Automount this token in pods."),
    ]

    def handle(self, quantum, project, codebase, ansible, args, deployment):
        msg = f"Create ServiceAccount {args.name} in {args.namespace}"
        playbook = ansible.playbook('k8s.iam', hosts='localhost',
            become=False, gather_facts=False, name='iam',
            run_once=True)
        task = playbook.task(namespace='k8s.iam',
            name=f"{args.namespace}-{args.name}",
            cls=KubernetesServiceAccountTask)
        task.setname(msg)
        task.setresourcename(args.name, part_of=project.symbolic_name)
        task.setnamespace(args.namespace)
        task.setautomount(args.automount)

        ansible.setenvfromtask('k8s.namespaces', args.namespace, task)
        with codebase.commit(msg):
            playbook.persist(codebase)
            quantum.persist(codebase)
