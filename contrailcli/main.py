"""
Command-line interface to the Contrail APIs
"""

import sys
import os
import network_vnc_api
import pkg_resources
import logging

from cliff.app import App
from cliff.commandmanager import CommandManager
from vnc_api import vnc_api


class ContrailCliApp(App):

    def __init__(self):
        super(ContrailCliApp, self).__init__(
            description=__doc__.strip(),
            version=pkg_resources.require('contrail-cli')[0].version,
            command_manager=CommandManager('contrailcli'))
        self.command_manager.add_command('net-show', network_vnc_api.ShowNetwork)
        self.command_manager.add_command('net-list', network_vnc_api.ListNetworks)
        self.command_manager.add_command('ipam-list', network_vnc_api.ListIPams)

    def build_option_parser(self, description, version):
        parser = super(ContrailCliApp, self).build_option_parser(description, version)
        parser.add_argument(
            '--contrail_ip', metavar='<contrail_ip>',
            default=os.environ.get('CONTRAIL_IP', None),
            help='Contrail API IP. Defaults to env[CONTRAIL_IP].')
        return parser

    def initialize_app(self, argv):
        logging.getLogger("requests").setLevel(logging.WARNING)

        if self.options.contrail_ip is None:
            raise Exception("You must provide a contrail controller IP via "
                "either --contrail_ip or via env[CONTRAIL_IP]")

        self.LOG.debug("CONTRAIL_IP=%s" % self.options.contrail_ip)
        self.vnc_lib = vnc_api.VncApi(api_server_host=self.options.contrail_ip)

    def clean_up(self, cmd, result, err):
        self.LOG.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.LOG.debug('got an error: %s', err)

def main(argv=sys.argv[1:]):
    myapp = ContrailCliApp()
    return myapp.run(argv)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
