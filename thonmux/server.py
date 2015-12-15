import logging
import os

from . import binding
from . import client
from . import exception
from . import session
from .misc import instance_factory

logger = logging.getLogger(__name__)


def _characterize():
    root = os.environ.get('TMUX_TMPDIR', None)
    if not root:
        root = os.environ.get('TMPDIR', None)
    if not root:
        root = os.path.join('/', 'tmp', 'tmux1000')
    logger.debug('Tmux (server) temp directory: ' + root)
    return root

_tmpdir = _characterize()


class Server:
    """The tmux server entity

    :param str socket_name: The name of the socket to be used to localize the
        tmux server
    :param socket_path: The path of the socket to be used to localize the tmux
        server
    :type socket_path: str or None

    :ivar list sessions: The list of sessions under the server
    :ivar list clients: The list of clients under the server
    """

    def __init__(self, socket_name='default', socket_path=None):
        prefix = []
        if socket_path:
            prefix.append('-S')
            prefix.append(socket_path)
            self.path = socket_path
        else:
            prefix.append('-L')
            prefix.append(socket_name)
            self.path = os.path.join(_tmpdir, socket_name)
        self.prefix = prefix

        try:
            logger.debug('Checking if tmux server is already running')
            self._execute('has-session')
            self.fresh = False
        except exception.EntityNotFound:
            logger.debug('Tmux server not running. Starting new tmux server')
            self._execute('new-session', dettached=True)
            self.fresh = True
        self._sync()
        logger.debug('Server instance started -> ' + str(self))

    def __repr__(self):
        return 'Server(path=%s)' % self.path

    def _sync(self):
        logger.debug('Synchronizing ' + str(self))
        output = self._execute('list-sessions')
        self.sessions = instance_factory(session.Session, parser=session.parse,
                                         parent=self, output=output)
        output = self._execute('list-clients')
        self.clients = instance_factory(client.Client, parser=client.parse,
                                        parent=self, output=output)
        return self

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
        self._execute('kill-server')

    def new_session(self, name, dettached=True, start_dir=None):
        xargs = []
        xargs.append('-s')
        xargs.append(name)
        if start_dir:
            xargs.append('-c')
            xargs.append(start_dir)
        self._execute('new-session', dettached=dettached, xargs=xargs)

    def find_session(self, name):
        matches = list(filter(lambda s: s.name == name, self.sessions))
        if len(matches) == 1:
            return matches[0]

    def attach_session(self, name):
        if self.fresh:
            session = self.sessions[0]
            session.rename(name)
        else:
            session = self.find_session(name)
            if not session:
                raise exception.SessionDoesNotExist
        return session
