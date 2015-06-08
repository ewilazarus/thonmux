from datetime import datetime
import logging
import re

from . import exception
from . import window
from .misc import instance_factory

logger = logging.getLogger(__name__)

_regex = re.compile((r"^(?P<name>.+):\s"
                    "\d+\swindows\s\(created\s\w+\s"
                    "(?P<timestr>\w+\s+\d+\s\d+:\d+:\d+\s\d+)\)"
                    "\s\["
                    "(?P<width>\d+)x(?P<height>\d+)"
                    ".*\]"
                    "(\s\((?P<attached>attached)\))?$"))


def parse(line):
    def parse_timestr(timestr):
        return datetime.strptime(timestr, '%b %d  %H:%M:%S %Y')

    kwargs = {}
    m = re.match(_regex, line)
    if m:
        kwargs['name'] = m.group('name')
        kwargs['creation'] = parse_timestr(m.group('timestr'))
        kwargs['width'] = int(m.group('width'))
        kwargs['height'] = int(m.group('height'))
        kwargs['attached'] = m.group('attached') is not None
    else:
        logger.debug('Failed to apply regex "%s" to the string "%s"' % (
                     _regex.pattern, line))
    return kwargs


class Session:
    """The tmux session entity

    :param parent: The parent server of the session
    :param str name: The name of the session
    :param datetime creation: The creation time of the session
    :param int height: The height of the session
    :param int width: The width of the session
    :param bool attached: The boolean describing if the session is attached or
        not

    :ivar list windows: The list of windows under the session
    :ivar active_window: The window that currently has focus on this session
    :vartype active_window: :class:`Window`
    """

    def __init__(self, parent, name, creation, height, width, attached):
        self.parent = parent
        self.name = name
        self.creation = creation
        self.height = height
        self.width = width
        self.attached = attached
        self._sync()
        logger.debug('Session instance created -> ' + str(self))

    def __repr__(self):
        return 'Session(name=%s, creation=%s, attached=%s)' % (
               self.name, self.creation, self.attached)

    @property
    def active_window(self):
        matches = list(filter(lambda w: w.active, self.windows))
        if len(matches) == 1:
            return matches[0]
        else:
            raise exception.EntityNotFound

    def _sync(self):
        logger.debug('Synchronizing ' + str(self))
        output = self._execute('list-windows')
        self.windows = instance_factory(window.Window, parser=window.parse,
                                        parent=self, output=output)
        return self

    def _execute(self, command, dettached=False, target=None, xargs=None):
        t = self.name + ':'
        if target:
            t += target
        return self.parent._execute(command, dettached, t, xargs)

    def attach(self):
        self._execute('attach-session')
        self.attached = True

    def kill(self):
        self._execute('kill-session')

    def rename(self, name):
        # TODO: slugfy(name)
        self._execute('rename-session', xargs=[name])
        self.name = name

    def new_window(self, name, start_dir=None, target=None):
        xargs = []
        xargs.append('-n')
        xargs.append(name)
        if start_dir:
            xargs.append('-c')
            xargs.append(start_dir)
        self._execute('new-window', target=target, xargs=xargs)
        raise exception.EntityOutOfSync

    def find_window(self, index):
        matches = list(filter(lambda w: w.index == index, self.windows))
        if len(matches) == 1:
            return matches[0]
        else:
            raise exception.EntityNotFound

    def select_window(self, index):
        w = self.find_window(index)
        w.select()

    def next_window(self):
        self._execute('next-window')
        raise exception.EntityOutOfSync

    def previous_window(self):
        self._execute('previous-window')
        raise exception.EntityOutOfSync

    def last_window(self):
        self._execute('last-window')
        raise exception.EntityOutOfSync
