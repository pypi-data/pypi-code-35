"""
.. Note::
   This plugin is scalable, i.e. usable in multiple pymania instances.

Add chat commands to be able to reload the configuration or plugins while the controller is running.
"""

import argparse
import pymania

class ReloadPlugin:
    """ Adds a chat command to reload the controller's config and/or plugins. """
    version = '1.0.0'
    name = 'reload'
    depends = 'chat', 'remote'

    async def load(self, plugin_config, dependencies):
        """ Defines the reload chat command. """
        chat = dependencies['chat']
        remote = dependencies['remote']

        parser = argparse.ArgumentParser('reload', description='Reloads the controller')
        parser.add_argument('--config', action='store_true', help='Reload the configuration script')
        parser.add_argument('--plugins', action='store_true', help='Reload the plugin modules')

        @chat.command(parser, plugin_config['privilege'])
        async def _chat_reload(from_, config, plugins):
            if not config and not plugins:
                await remote.send_message(plugin_config['missing_option'], from_.login)
                return

            items = []
            flags = pymania.ControllerState(0)
            if config:
                items.append('configuration')
                flags = flags | pymania.ControllerState.RELOAD_CONFIG
            if plugins:
                items.append('plugins')
                flags = flags | pymania.ControllerState.RELOAD_PLUGINS
            await remote.send_message(
                plugin_config['message'].format(player=from_.nickname, items=', '.join(items)),
                from_.login
            )

            raise pymania.ControllerInterrupt(flags, f'{from_.login} issued a reload command')
