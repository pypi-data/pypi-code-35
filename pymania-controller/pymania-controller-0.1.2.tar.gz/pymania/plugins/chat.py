"""
.. Note::
   This plugin is scalable, i.e. usable in multiple pymania instances.

Handles chat commands and the visual appearance of messages. Registering a chat command is as simple
as follows:

.. code-block:: python

    chat = dependencies['chat']
    remote = dependencies['remote']
    players = dependencies['players']

    parser = argparse.ArgumentParser('hi', description='Say hi to everyone')
    parser.add_argument('login', nargs='?', help='Login of the player to say hi to')

    @chat.command(parser, config['privilege_to_say_hi'])
    async def say_hi(from_, login): # from is always a Player object
        if login is not None:
            player = players.get(login)
            if player is None:
                await remote.send_message(f'{login} is not a valid player', from_.login)
            else:
                await remote.send_message(f'Hello {player.nickname}!')
        else:
            await remote.send_message(f'Hello everyone!')

Using Python's `ArgumentParser` has multiple advantages:

- The argument name determines the name of the corresponding keyword argument in the handler
- Automatically generate help for that command
- Rapidly make something that just works

"""

import collections
import logging

import defusedxml.xmlrpc as defused_xmlrpc

Command = collections.namedtuple('Command', ['argparser', 'privileges', 'handler'])

class _ArgumentError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class ChatPlugin:
    """ Manages chat commands and chat messages in general. """
    version = '1.0.0'
    name = 'chat'
    depends = 'remote', 'players'
    logger = logging.getLogger(__name__)

    __slots__ = '_commands', '_route_default_chat'

    def __init__(self):
        self._commands = {}
        self._route_default_chat = True

    async def load(self, config, dependencies):
        """ Creates a handler for the TrackMania.PlayerChat callback. """
        remote = dependencies['remote']
        players = dependencies['players']

        # disable sending the default-formatted message by the dedicated server
        try:
            await remote.execute('ChatEnableManualRouting', True, True)
        except defused_xmlrpc.xmlrpc_client.Fault:
            self._route_default_chat = False # prevent duplicated 'default' chat messages

        @remote.callback('TrackMania.PlayerChat')
        async def _chat(_uid, login, text, *_args):
            text = text.strip()
            player = players.get(login)

            if not text or not int(player.privileges) & config['privilege'].value:
                # prevent spamming empty and a muted player's messages
                return
            prefix = config['command_prefix']
            if not text.startswith(prefix) and self._route_default_chat: # normal chat message
                await remote.send_message(
                    config['message'].format(player=player.nickname, message=text),
                    login
                )
                return
            args = [x for x in text[len(prefix):].split(' ') if x]
            if not args: # an empty command is not worth notifying of
                return

            try: # command was used
                cmd = self._commands[args[0]]
                if cmd.privileges is None or int(player.privileges) & cmd.privileges.value:
                    if '-h' in args or '--help' in args:
                        # pylint: disable=line-too-long
                        usage = cmd.argparser.format_usage().replace('usage: ', prefix).replace('\n', '')
                        await remote.send_message(config['command_usage'].format(usage=usage), login)
                        return
                    try:
                        args = args[1:]
                    except IndexError:
                        args = []
                    try:
                        await cmd.handler(player, **vars(cmd.argparser.parse_args(args)))
                    except _ArgumentError as exc:
                        await remote.send_message(
                            config['command_error'].format(message=exc.message),
                            login
                        )
                else: # no privileges
                    await remote.send_message(
                        config['missing_privilege'].format(
                            privileges=cmd.privileges,
                            command=args[0]
                        ),
                        login
                    )
            except KeyError: # unregistered command
                await remote.send_message(config['invalid_command'].format(command=args[0]), login)

    async def unload(self):
        """ Clears all commands. """
        self._commands.clear()

    def command(self, argparser, privileges=None):
        """ Adds a command.

        :param argparser: argparse.ArgumentParser to use for parsing the arguments
        :param privileges: Required privilege(s) to execute the command
        """
        def _error(message):
            raise _ArgumentError(message)
        def _decorator(function):
            argparser.error = _error
            self._commands[argparser.prog] = Command(argparser, privileges, function)
            self.logger.info('Registered chat command "%s"', argparser.prog)
            return function
        return _decorator
