import logging
import re

from misc import instance_factory
import pane

logger = logging.getLogger(__name__)

_regex = re.compile((r"^(?P<index>\d+):\s"
                     "(?P<name>.*?)"
                     "(?P<status>-|\*)?\s"
                     ".*$"))


def parse(line):
    def parse_status(raw_status):
        if raw_status:
            status = 'active'
            if raw_status == '-':
                status = 'last'
            return status

    kwargs = {}
    m = re.match(_regex, line)
    if m:
        kwargs['index'] = m.group('index')
        kwargs['name'] = m.group('name')
        kwargs['status'] = parse_status(m.group('status'))
    else:
        logger.debug('Failed to apply regex "%s" to the string "%s"' % (
                     _regex.pattern, line))
    return kwargs


class Window:

    def __init__(self, parent, index, name, status):
        self.parent = parent
        self.index = index
        self.name = name
        self.status = status
        logger.debug('Window instance created -> ' + str(self))

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
        t = self.index
        if target:
            t += ('.' + target)
        return self.parent._execute(command, dettached, t, xargs)

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
        return instance_factory(pane.Pane, parser=pane.parse,
                                parent=self, output=output)
