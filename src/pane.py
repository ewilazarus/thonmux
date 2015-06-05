import logging
import re

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
        r = 'Pane(index=%s, dimensions=[%dx%d])' % (self.index, self.width,
                                                    self.height)
        if self.active:
            r += '*'
        return r

    def _execute(self, command, dettached=False, target=None, xargs=None):
        return self.parent._execute(command, target=self.index, xargs=xargs)

    def select(self):
        self._execute('select-pane')
        self.active = True

    def kill(self):
        self._execute('kill-pane')
        self.parent._sync()

    def send_keys(self, keys, enter=True):
        self._execute('send-keys', xargs=[keys])
        if enter:
            self._execute('send-keys', xargs=['C-m'])
