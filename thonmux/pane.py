import logging
import re

from . import exception

logger = logging.getLogger(__name__)

_regex = re.compile((r"^(?P<index>\d+):\s"
                     "\[(?P<width>\d+)x(?P<height>\d+)\]"
                     ".*?"
                     "(\((?P<active>active)\))?$"))


def parse(line):
    kwargs = {}
    m = re.match(_regex, line)
    if m:
        kwargs['index'] = m.group('index')
        kwargs['width'] = int(m.group('width'))
        kwargs['height'] = int(m.group('height'))
        kwargs['active'] = m.group('active') is not None
    else:
        logger.debug('Failed to apply regex "%s" to the string "%s"' % (
                     _regex.pattern, line))
    return kwargs


class Pane:
    """The tmux pane entity

    :param parent: The parent window of the pane
    :type parent: :class:`Window`
    :param int index: The index of the pane
    :param int width: The width of the pane
    :param int height: The height of the pane
    :param bool active: The boolean describing if the pane is active or not
    """

    def __init__(self, parent, index, width, height, active):
        self.parent = parent
        self.index = index
        self.width = width
        self.height = height
        self.active = active
        logger.debug('Pane instance created -> ' + str(self))

    def __lt__(self, other):
        return self.index < other.index

    def __repr__(self):
        return 'Pane(index=%s, dimensions=[%dx%d], active=%s)' % (
               self.index, self.width, self.height, self.active)

    def _execute(self, command, target=None, xargs=None):
        t = target or self.index
        return self.parent._execute(command, target=t, xargs=xargs)

    def select(self):
        self._execute('select-pane')
        self.active = True

    def kill(self):
        self._execute('kill-pane')
        raise exception.EntityOutOfSync

    def resize(self, width, height, xargs=None):
        if not xargs:
            xargs = []
            xargs.append('-x')
            xargs.append(width)
            xargs.append('-y')
            xargs.append(height)
        self._execute('resize-pane', xargs=xargs)

    def zoom(self):
        self.resize(None, None, ['-Z'])

    def send_keys(self, keys, enter=True):
        self._execute('send-keys', xargs=[keys])
        if enter:
            self._execute('send-keys', xargs=['C-m'])

    def next(self):
        self._execute('select-pane', target='.+')
        raise exception.EntityOutOfSync

    def previous(self):
        self._execute('select-pane', target='.-')
        raise exception.EntityOutOfSync
