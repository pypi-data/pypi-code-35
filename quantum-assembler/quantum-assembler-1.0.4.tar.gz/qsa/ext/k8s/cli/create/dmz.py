"""Create a DMZ using ``Namespace`` and ``NetworkPolicy``
resources.
"""
import ioc

from qsa.lib.cli import Command
from qsa.lib.cli import Enable
from qsa.lib.cli import Argument
from qsa.lib.cli import ArgumentList
from qsa.ext.k8s.network import GKELoadbalancerBuilder
from qsa.ext.k8s.network import BaremetalLoadBalancerBuilder


class CreateDemilitarizedZoneCommand(Command):
    command_name = 'dmz'
    builders = {
        'gke': GKELoadbalancerBuilder,
        'baremetal': BaremetalLoadBalancerBuilder
    }
    codebase = ioc.class_property('core:CodeRepository')
    repository = ioc.class_property('ansible:TaskRepository')
    args = [
        Argument('name', help="the name of the DMZ."),
        Argument('--addr',
            help="the IP address of the load balancer, if applicable."),
        ArgumentList('--src', dest='ranges',
            help="the allowed source address ranges."),
        Enable('--unbound',
            help="do not bind this namespace to a specific environment."),
        Enable('--internal', action='store_true',
            help="the load balancer is internal."),
        Argument('--platform', help="specifies the platform.",
            choices=builders.keys()),
        ArgumentList('-p', dest='ports',
            help="specifies the ports that are allowed to connect."),
        ArgumentList('-e', dest='environments',
            help="the environments to deploy the DMZ in."),
    ]

    def handle(self, args, quantum):
        if not args.environments:
            self.fail("Specify at least one environment using the -e parameter")
        msg = f"Create load balancer {args.name}"
        msg += f' ({", ".join(args.environments)})'
        LoadbalancerBuilder = self.builders[args.platform]
        with self.codebase.commit(msg, noprefix=True):
            LoadbalancerBuilder.build(args.name, addr=args.addr,
                ranges=args.ranges, unbound=args.unbound,
                internal=args.internal, ports=args.ports,
                environments=args.environments)
            quantum.persist()
