import logging

from binding import Binding
import exception
import session

logger = logging.getLogger(__name__)


class Server:
    id = -1

    def __init__(self, socket_name=None, socket_path=None):
        logger.info('Attempting to start tmux server instance')
        prefix = []
        if socket_name:
            prefix.append('-L')
            prefix.append(socket_name)
        if socket_path:
            prefix.append('-S')
            prefix.append(socket_path)

        self.socket_name = socket_name
        self.socket_path = socket_path
        self.prefix = prefix

        try:
            logger.info('Checking if tmux server is already running')
            self._execute('has-session')
        except exception.ServerNotFound:
            logger.info('Tmux server not running. Starting new tmux server')
            self._execute('new-session', dettached=True)

        self.id += 1
        logger.info('Server instance successfully started')

    def __repr__(self):
        return 'Server(id=%s)' % self.id

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

        b = Binding()
        b.run(final_command)
        return b.stdout

    def kill(self):
        # TODO: for s in self.sessions: s.kill()
        self._execute('kill-server')

    @property
    def sessions(self):
        output = self._execute('list-sessions')
        return session.factory(output, parent=self)
