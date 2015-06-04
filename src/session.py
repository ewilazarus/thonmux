from datetime import datetime
import logging
import re

from misc import instance_factory
import window

logger = logging.getLogger(__name__)

_regex = re.compile((r"^(?P<name>.+):\s"
                    "\d+\swindows\s\(created\s\w+\s"
                    "(?P<timestr>\w+\s+\d+\s\d+:\d+:\d+\s\d+)\)"
                    "\s\["
                    "(?P<width>\d+)x(?P<height>\d+)"
                    ".*\]"
                    "(\s\((?P<attached>attached)\))?$"))


def parse(line):
    kwargs = {}
    m = re.match(_regex, line)
    if m:
        kwargs['name'] = m.group('name')
        timestr = m.group('timestr')
        timestamp = datetime.strptime(timestr, '%b %d  %H:%M:%S %Y')
        kwargs['timestamp'] = timestamp
        kwargs['width'] = int(m.group('width'))
        kwargs['height'] = int(m.group('height'))
        kwargs['attached'] = m.group('attached') is not None
    else:
        logger.debug('Failed to apply regex "%s" to the string "%s"' % (
                     _regex.pattern, line))
    return kwargs


class Session:

    def __init__(self, parent, name, timestamp, height, width, attached):
        logger.info('Attempting to create session instance (name=%s)' % name)
        self.parent = parent
        self.name = name
        self.creation = timestamp
        self.height = height
        self.width = width
        self.attached = attached
        logger.info('Session instance successfully created')

    def __repr__(self):
        r = 'Session(name=%s, creation=%s)' % (self.name, self.creation)
        if self.attached:
            r += '*'
        return r

    def _execute(self, command, dettached=False, target=None, xargs=None):
        if target:
            target = self.name + ':' + target
        else:
            target = self.name
        return self.parent._execute(command, dettached, target, xargs)

    def attach(self):
        self._execute('attach-session')
        self.attached = True

    def kill(self):
        # TODO: for w in self.windows: w.kill()
        self._execute('kill-session')
        del(self.parent)     # remove unwanted reference to Server object

    def rename(self, name):
        # TODO: slugfy(name)
        self._execute('rename-session', xargs=[name])
        self.name = name

    @property
    def windows(self):
        output = self._execute('list-windows')
        return instance_factory(window.Window, parser=window.parse,
                                parent=self, output=output)
