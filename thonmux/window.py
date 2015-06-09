import logging
import re

from . import exception
from . import pane
from .misc import instance_factory

logger = logging.getLogger(__name__)

_regex = re.compile((r"^(?P<index>\d+):\s"
                     "(?P<name>.*?)"
                     "(?P<status>-|\*)?\s"
                     ".*$"))


def parse(line):
    def parse_status(raw_status):
        if raw_status:
            return raw_status == '*'
        return False

    kwargs = {}
    m = re.match(_regex, line)
    if m:
        kwargs['index'] = m.group('index')
        kwargs['name'] = m.group('name')
        kwargs['active'] = parse_status(m.group('status'))
    else:
        logger.debug('Failed to apply regex "%s" to the string "%s"' % (
                     _regex.pattern, line))
    return kwargs


class Window:
    """The tmux window entity

    :param parent: The parent session of the window
    :type parent: :class:`Session`
    :param str index: The index of the window
    :param str name: The name of the window
    :param bool active: The boolean describing if the window is active or not

    :ivar list panes: The list of panes under the window
    :ivar active_pane: The pane that currently has focus on the window
    :vartype active_pane: :class:`Pane`
    """

    def __init__(self, parent, index, name, active):
        self.parent = parent
        self.index = index
        self.name = name
        self.active = active
        self._sync()
        logger.debug('Window instance created -> ' + str(self))

    def __lt__(self, other):
        return self.index < other.index

    def __repr__(self):
        return 'Window(index=%s, name=%s, dimensions=[%sx%s], active=%s)' % (
               self.index, self.name, self.width, self.height, self.active)

    @property
    def active_pane(self):
        matches = list(filter(lambda p: p.active, self.panes))
        if len(matches) == 1:
            return matches[0]
        else:
            raise exception.EntityNotFound

    @property
    def height(self):
        return self.parent.height

    @property
    def width(self):
        return self.parent.width

    def _sync(self):
        logger.debug('Synchronizing ' + str(self))
        output = self._execute('list-panes')
        self.panes = instance_factory(pane.Pane, parser=pane.parse,
                                      parent=self, output=output)
        return self

    def _execute(self, command, target=None, xargs=None):
        t = self.index
        if target:
            t += ('.' + target)
        return self.parent._execute(command, target=t, xargs=xargs)

    def kill(self):
        self._execute('kill-window')
        raise exception.EntityOutOfSync

    def rename(self, name):
        # TODO: slugfy(name)
        self._execute('rename-window', xargs=[name])
        self.name = name

    def split(self, horizontal=False, start_dir=None, target=None):
        xargs = []
        if horizontal:
            xargs.append('-h')
        if start_dir:
            xargs.append('-c')
            xargs.append(start_dir)
        self._execute('split-window', target=target, xargs=xargs)
        raise exception.EntityOutOfSync

    def select(self, xargs=None):
        self._execute('select-window', xargs=xargs)
        self.active = True

    def find_pane(self, index):
        matches = list(filter(lambda p: p.index == index, self.panes))
        if len(matches) == 1:
            return matches[0]
        else:
            raise exception.EntityNotFound

    def select_pane(self, index):
        p = self.find_pane(index)
        p.select()
        raise exception.EntityOutOfSync
