import logging
import sys
import requests
import urlparse
import pprint

from cliff.show import ShowOne
from cliff.command import Command
from cliff.lister import Lister
from uuid import UUID
from cfgm_common.exceptions import NoIdError

log = logging.getLogger(__name__)

class ContrailAction:

    def is_uuid(self, s):
        try:
            UUID(s, version=4)
            return True
        except ValueError:
            return False

    def get_network(self, network_ref):
        if self.is_uuid(network_ref):
            kwargs = {'id': network_ref}
            network_ref_type = 'uuid'
        else:
            kwargs = {'fq_name_str': network_ref}
            network_ref_type = 'name'

        try:
            return self.app.vnc_lib.virtual_network_read(**kwargs)
        except NoIdError as e:
            raise Exception("No network with %s %s" %
                (network_ref_type, network_ref))


class ShowNetwork(ShowOne, ContrailAction):
    """show network details"""

    def get_parser(self, prog_name):
        parser = super(ShowNetwork, self).get_parser(prog_name)
        parser.add_argument('network')
        return parser

    def take_action(self, parsed_args):
        network = self.get_network(parsed_args.network)

        columns = ('uuid',
                   'fq_name',
                   'display_name',
                   'router_external',
                   'is_shared')

        data = (network.uuid,
                ':'.join(network.fq_name),
                network.display_name,
                network.router_external or False,
                network.is_shared or False)

        return (columns, data)


class ListNetworks(Lister, ContrailAction):
    """List all networks"""

    def take_action(self, parsed_args):
        networks = self.app.vnc_lib.virtual_networks_list()['virtual-networks']
        return (('uuid', 'fq_name'),
                ((net['uuid'], ':'.join(net['fq_name'])) for net in networks)
                )


class ListIPams(Lister, ContrailAction):
    """List all IPAMs for a given network"""

    def get_parser(self, prog_name):
        parser = super(ListIPams, self).get_parser(prog_name)
        parser.add_argument('network_uuid',
            help='UUID of network to list subnets for')
        return parser

    def take_action(self, parsed_args):
        network = self.get_network(parsed_args.network_uuid)

        columns = ('fq_name', 'uuid', 'ip_prefix', 'ip_prefix_len', 'gateway',
            'dns')

        data = []
        for ipam_ref in network.get_network_ipam_refs():
            for ipam_subnet in ipam_ref['attr'].get_ipam_subnets():
                ip_prefix = ipam_subnet.get_subnet().ip_prefix
                ip_prefix_len = ipam_subnet.get_subnet().ip_prefix_len

                data.append((':'.join(ipam_ref['to']),
                             ipam_ref['uuid'],
                             ip_prefix,
                             ip_prefix_len,
                             ipam_subnet.get_default_gateway(),
                             ipam_subnet.get_dns_server_address()))

        return (columns, data)
