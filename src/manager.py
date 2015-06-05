import inspect
from functools import wraps
import logging

from exception import EntityOutOfSync

logger = logging.getLogger(__name__)

_watched_methods = ['new_window', 'select_window', 'next_window',
                    'previous_window', 'last_window', 'kill_window',
                    'window_split', 'select_pane', 'kill_pane']


def synchronous(cls):
    def action(f):
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            try:
                return f(self, *args, **kwargs)
            except EntityOutOfSync:
                if not self.watch[f.__name__]:
                    self.sync()
                    self.watch[f.__name__] = True
                    return f(self, *args, **kwargs)
                self.watch[f.__name__] = False
        return wrapper

    watch = {}
    for name, member in inspect.getmembers(cls):
        if name in _watched_methods:
            watch[name] = False
            setattr(cls, name, action(member))

    init = cls.__init__
    def __init__(self, *args, **kwargs):
        init(self, *args, **kwargs)
        setattr(cls, 'watch', watch)
    cls.__init__ = __init__
    return cls


@synchronous
class Manager:

    def __init__(self, session):
        self._session = session
        self.sync(False)
        logger.debug('Browser instance created -> ' + str(self))

    def __repr__(self):
        return 'Browser(session=%s, window=%s, pane=%s)' % (self._session,
                                                            self._window,
                                                            self._pane)

    def sync(self, session=True):
        if session:
            self._session = self._session._sync()
        self._window = self._session.active_window
        self._pane = self._window.active_pane
        logger.debug('Synchronizing Manager: ' + str(self))

    @property
    def session_name(self):
        return self._session.name

    def kill_session(self, name):
        self._session.kill()

    def rename_session(self, name):
        self._session.rename(name)

    @property
    def window_name(self):
        return self._window.name

    @property
    def window_index(self):
        return self._window.index

    def new_window(self, name, start_dir=None, target=None):
        self._session.new_window(name, start_dir, target)

    def select_window(self, index):
        self._session.select_window(index)

    def next_window(self):
        self._window = self._session.next_window()

    def previous_window(self):
        self._session.previous_window()

    def last_window(self):
        self._session.last_window()

    def rename_window(self, name):
        self._window.rename(name)

    def kill_window(self):
        self._window.kill()

    def window_split(self, horizontal=False, start_dir=None, target=None):
        self._window.split(horizontal, start_dir, target)

    @property
    def pane_index(self):
        return self._pane.index

    def select_pane(self, index):
        self._window.select_pane(index)

    def kill_pane(self):
        self._pane.kill()

    def send_keys(self, keys, enter=True):
        self._pane.send_keys(keys, enter)


if __name__ == '__main__':
    import logging, sys
    import server

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    sv = server.Server()
    s = sv.find_session('0')

    m = Manager(s)
    import pdb; pdb.set_trace()
