import logging

from misc import synchronous
from server import Server

logger = logging.getLogger(__name__)


@synchronous
class Thonmux:
    """class:: Thonmux(session_name[, socket_name='default', socket_path=None])
    **The** "tmux" interface.

    This class prevents that interactions with "tmux" result in an out of sync
    entity tree, where the python objects representation differ from what
    really exists in "tmux".

    It works by keeping track of the *session* provided to its constructor, as
    well as of to its active *window* and active *pane*. Whenever an action
    that would alter the tree's state happens, it raises an `exception.Entity
    OutOfSync` that is handled by reconstructing the tree and updating the
    references of the tracked *session*, *window* and *pane*.

    All "tmux" commands are run against the tracked *session*, *window* and
    *pane* as needed.

    Currently, there's support for the following "tmux" command:
    - kill-session
    - rename-session
    - new-window
    - select-window
    - next-window
    - previous-window
    - last-window
    - rename-window
    - kill-window
    - window-split
    - select-pane
    - kill-pane
    - resize-pane
    - send-keys

    There's also a convenience command:
    - toggle-zoom (zooms in/out of the tracked *pane*)

    :param str session_name: The name of target session. If a session with the
    provided name already exists, it will attach to it. Otherwise, it will
    create a new session with the provided name.
    :param str socket_name: The name of the socket to be used to localize the
    "tmux" server.
    :param socket_path: The path of the socket to be used to localize the
    "tmux" server.
    :type socket_path: str or None

    Refer to the `"tmux" manual<http://www.openbsd.org/cgi-bin/man.cgi/OpenBSD-
    current/man1/tmux.1?query=tmux&sec=1>`_ for more information.
    """

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

    def resize_pane(self, width, height):
        self.pane.resize(width, height)

    def send_keys(self, keys, enter=True):
        self.pane.send_keys(keys, enter)

    def toggle_zoom(self):
        self.pane.zoom()
