import logging
import re

logger = logging.getLogger(__name__)

_regex = re.compile((r"^(?P<path>.+?):\s"
                     "(?P<session_name>.+?)\s"
                     "\[\d+x\d+\s"
                     "(?P<terminal>.+?)\]\s"
                     "\((?P<encoding>.+?)\)$"))


def parse(line):
    kwargs = {}
    m = re.match(_regex, line)
    if m:
        kwargs['path'] = m.group('path')
        kwargs['session_name'] = m.group('session_name')
        kwargs['terminal'] = m.group('terminal')
        kwargs['encoding'] = m.group('encoding')
    else:
        logger.debug('Failed to apply regex "%s" to the string "%s"' % (
                     _regex.pattern, line))
    return kwargs


class Client:
    """The tmux client entity

    :param parent: The parent server of the client
    :type parent: :class:`server.Server`
    :param str path: The path to the client
    :param str terminal: The terminal flavour used by the client
    :param str encoding: The encoding used by the client
    :param str session_name: The name of the session the client is attached to
    """

    def __init__(self, parent, path, terminal, encoding, session_name):
        self.parent = parent
        self.path = path
        self.terminal = terminal
        self.encoding = encoding
        self.session = parent.find_session(session_name)
        logger.debug('Client instance created -> ' + str(self))

    def __repr__(self):
        return ('Client(path=%s, terminal=%s, encoding=%s,'
                'session=%s)' % (self.path, self.terminal, self.encoding,
                                 self.session))

    def _execute(self, command, dettached=False, target=None, xargs=None):
        self.parent._execute(command, dettached, self.path, xargs)

    def detach(self):
        self._execute('detach-client')
        self.parent._sync()
