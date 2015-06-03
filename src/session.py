from datetime import datetime
import logging
import re

logger = logging.getLogger(__name__)

_regex = re.compile((r"^(?P<name>.+):\s"
                    "\d+\swindows\s\(created\s\w+\s"
                    "(?P<timestr>\w+\s+\d+\s\d+:\d+:\d+\s\d+)\)"
                    "\s\[.*\]"
                    "(\s\((?P<attached>attached)\))?$"))


def _parse(line):
    kwargs = {}
    m = re.match(_regex, line)
    if m:
        kwargs['name'] = m.group('name')
        timestr = m.group('timestr')
        timestamp = datetime.strptime(timestr, '%b %d  %H:%M:%S %Y')
        kwargs['timestamp'] = timestamp
        kwargs['attached'] = m.group('attached') is not None
    else:
        logger.debug('Failed to apply regex "%s" in the string "%s"' % (
                     _regex.pattern, line))
    return kwargs


def factory(output, parent):
    sessions = []
    for line in output:
        kwargs = _parse(line)
        sessions.append(Session(parent, **kwargs))
    return sessions


class Session:

    def __init__(self, parent, name, timestamp, attached):
        logger.info('Attempting to create session instance (name=%s)' % name)
        self.parent = parent
        self.name = name
        self.creation = timestamp
        self.attached = attached
        logger.info('Session instance successfully created')

    def __repr__(self):
        if self.attached:
            r = 'Session(name=%s, creation=%s)*' % (self.name, self.creation)
        else:
            r = 'Session(name=%s, creation=%s)' % (self.name, self.creation)
        return r

    # TODO: Tentar fazer __call__ e testar se o parent e nulo. Se for, entao
    #       significa que ele esta criando uma sessao a partir de um comando
    #       ao inves de a partir da factory.

    def execute(self, command, dettached=False, target=None, xargs=None):
        if not target:
            target = self.name
        else:
            target = self.name + ':' + target
        self.parent.execute(command, dettached=dettached, target=target,
                            xargs=xargs)

    def attach(self):
        self.execute('attach-session')

    def detach(self):
        self.parent.execute('detach-client', xargs=['-s', self.name])

    def kill(self):
        self.execute('kill-session')

    def rename(self, name):
        # TODO: slugfy(name)
        self.execute('rename-session', xargs=[name])
