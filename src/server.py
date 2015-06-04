import logging
import os

import binding
import client
import exception
from misc import instance_factory
import session

logger = logging.getLogger(__name__)


def _characterize(socket_name):
    root = os.environ.get('TMUX_TMPDIR', None)
    if not root:
        root = os.environ.get('TMPDIR', None)
    if not root:
        root = os.path.join('/', 'tmp', 'tmux1000')
    return os.path.join(root, socket_name)


class Server:

    def __init__(self, socket_name='default', socket_path=None):
        logger.info('Attempting to start tmux server instance')
        prefix = []
        if socket_path:
            prefix.append('-S')
            prefix.append(socket_path)
            self.path = socket_path
        else:
            prefix.append('-L')
            prefix.append(socket_name)
            self.path = _characterize(socket_name)
        self.prefix = prefix

        try:
            logger.info('Checking if tmux server is already running')
            self._execute('has-session')
        except exception.ServerNotFound:
            logger.info('Tmux server not running. Starting new tmux server')
            self._execute('new-session', dettached=True)
        logger.info('Server instance successfully started')

    def __repr__(self):
        return 'Server(path=%s)' % self.path

    def _execute(self, command, dettached=False, target=None, xargs=None):
        final_command = self.prefix[:]
        final_command += [command]
        if dettached:
            final_command.append('-d')
        if target:
            final_command.append('-t')
            final_command.append(target)
        if xargs:
            final_command += xargs
        return binding.run(final_command)

    def kill(self):
        # TODO: for s in self.sessions: s.kill()
        self._execute('kill-server')

    @property
    def sessions(self):
        output = self._execute('list-sessions')
        return instance_factory(session.Session, parser=session.parse,
                                parent=self, output=output)

    @property
    def clients(self):
        output = self._execute('list-clients')
        return instance_factory(client.Client, parser=client.parse,
                                parent=self, output=output)
