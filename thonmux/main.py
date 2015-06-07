import logging

from misc import synchronous
from server import Server

logger = logging.getLogger(__name__)


@synchronous
class Thonmux:

    def __init__(self, session_name, socket_name='default', socket_path=None):
        server = Server(socket_name, socket_path)
        self.session = server.attach_session(session_name)
        self._sync(False)
        logger.debug('Thonmux instance created -> ' + str(self))

    def __repr__(self):
        return 'Thonmux[%s, %s, %s]' % (self.session, self.window, self.pane)

    def _sync(self, session=True):
        if session:
            self.session = self.session._sync()
        self.window = self.session.active_window
        self.pane = self.window.active_pane
        logger.debug('Synchronizing Thonmux: ' + str(self))

    def kill_session(self, name):
        self.session.kill()

    def rename_session(self, name):
        self.session.rename(name)

    def new_window(self, name, start_dir=None, target=None):
        self.session.new_window(name, start_dir, target)

    def select_window(self, index):
        self.session.select_window(index)

    def next_window(self):
        self.session.next_window()

    def previous_window(self):
        self.session.previous_window()

    def last_window(self):
        self.session.last_window()

    def rename_window(self, name):
        self.window.rename(name)

    def kill_window(self):
        self.window.kill()

    def window_split(self, horizontal=False, start_dir=None, target=None):
        self.window.split(horizontal, start_dir, target)

    def select_pane(self, index):
        self.window.select_pane(index)

    def kill_pane(self):
        self.pane.kill()

    def toggle_zoom(self):
        self.pane.zoom()

    def resize_pane(self, width, height):
        self.pane.resize(width, height)

    def send_keys(self, keys, enter=True):
        self.pane.send_keys(keys, enter)
