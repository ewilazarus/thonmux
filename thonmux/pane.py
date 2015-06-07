import logging
import re

import exception

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
    """class:Pane(parent, index, width, height, active)
    :param parent: The parent window of the pane
    :param type: Window
    :param int index: The index of the pane
    :param int width: The width of the pane
    :param int height: The height of the pane
    :param bool active: The boolean describing if the pane is active or not

    The tmux pane entity.
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

    def _execute(self, command, xargs=None):
        return self.parent._execute(command, target=self.index, xargs=xargs)

    def select(self):
        """method:: select()

        Selects the pane
        """
        self._execute('select-pane')
        self.active = True

    def kill(self):
        """method:: kill()
        :raises exception.EntityOutOfSync:

        Kills the pane
        """
        self._execute('kill-pane')
        raise exception.EntityOutOfSync

    def resize(self, x, y, xargs=None):
        """method: resize(x, y[, xargs])
        :param int x: The target width of the pane
        :param int y: The target height of the pane
        :param xargs: Additional flags of the 'resize-pane' command
        :type xargs: list or None

        Resized the pane
        """
        if not xargs:
            xargs = []
            xargs.append('-x')
            xargs.append(x)
            xargs.append('-y')
            xargs.append(y)
        self._execute('resize-pane', xargs=xargs)

    def zoom(self):
        """method: zoom()

        Toggles zoom of the pane
        """
        self.resize(None, None, ['-Z'])

    def send_keys(self, keys, enter=True):
        """method: send_keys(keys[, enter=True])
        :param str keys: The key sequence to be sent to the pane
        :param bool enter: If True, sends an enter after the :param:keys
        """
        self._execute('send-keys', xargs=[keys])
        if enter:
            self._execute('send-keys', xargs=['C-m'])
