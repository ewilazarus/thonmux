import logging
import re

import pane

logger = logging.getLogger(__name__)

_regex = re.compile((r"^(?P<index>\d+):\s"
                     "(?P<name>.*?)"
                     "(?P<status>-|\*)?\s"
                     ".*$"))


def _parse(line):
    def parse_status(raw_status):
        if raw_status:
            if raw_status == '*':
                status = 'active'
            else:
                status = 'last'
            return status

    kwargs = {}
    m = re.match(_regex, line)
    if m:
        kwargs['index'] = m.group('index')
        kwargs['name'] = m.group('name')
        kwargs['status'] = parse_status(m.group('status'))
    else:
        logger.debug('Failed to apply regex "%s" in the string "%s"' % (
                     _regex.pattern, line))
    return kwargs


def factory(output, parent):
    windows = []
    for line in output:
        kwargs = _parse(line)
        windows.append(Window(parent, **kwargs))
    return windows


class Window:

    def __init__(self, parent, index, name, status):
        logger.info('Attempting to create window instance (index=%s)' % index)
        self.parent = parent
        self.index = index
        self.name = name
        self.status = status
        logger.info('Window instance successfully created')

    def __lt__(self, other):
        return self.index < other.index

    def __repr__(self):
        r = 'Window(index=%s, name=%s, dimensions=[%sx%s])' % (self.index,
                                                               self.name,
                                                               self.width,
                                                               self.height)
        if self.status:
            if self.status == 'active':
                r += '*'
            else:
                r += '-'
        return r

    def _execute(self, command, dettached=False, target=None, xargs=None):
        if not target:
            target = self.index
        else:
            target = self.index + '.' + target
        return self.parent._execute(command, dettached, target, xargs)

    def select(self):
        self._execute('select-window')
        self.status = 'active'

    def kill(self):
        # TODO: for p in self.panes: p.kill()
        self._execute('kill-window')
        del(self.parent)

    def rename(self, name):
        # TODO: slugfy(name)
        self._execute('rename-window', xargs=[name])
        self.name = name

    @property
    def height(self):
        return self.parent.height

    @property
    def width(self):
        return self.parent.width

    @property
    def panes(self):
        output = self._execute('list-panes')
        return pane.factory(output, parent=self)
