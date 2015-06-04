import logging
import re

logger = logging.getLogger(__name__)

_regex = re.compile((r"^(?P<path>.*?):\s"
                     "(?P<session_name>\d+)\s"
                     "\[\d+x\d+\s"
                     "(?P<terminal>.*?)\]\s"
                     "\((?P<encoding>.*?)\)$"))


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

    def __init__(self, path, terminal, encoding, session_name):
        logger.info('Attempting to create client instance (path=%s)' % path)
        self.path = path
        self.terminal = terminal
        self.encoding = encoding
        self.session_name = session_name
        logger.info('Client instance successfully created')

    def __repr__(self):
        return ('Client(path=%s, terminal=%s, encoding=%s,'
                'session=%s)' % (self.path, self.terminal, self.encoding,
                                 self.session_name))

    def _execute(self, command, dettached=False, target=None, xargs=None):
        pass
        # TODO: Criar execute
