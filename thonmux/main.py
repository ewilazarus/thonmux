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
    well as to its active *window* and active *pane*. Whenever an action that
    would alter the tree's state happens, it raises an `exception.EntityOutOf
    Sync`_ that is handled by reconstructing the tree and updating the
    references of the tracked *session*, *window* and *pane*.

    All "tmux" commands are run against the tracked *session*, *window* and
    *pane* as needed.

    Currently, there's support for the following "tmux" command:
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

    def rename_session(self, name):
        """method:: rename_session(name)
        Renames the tracked *session*.

        :param str name: The name to be applied to the session
        """
        self.session.rename(name)

    def new_window(self, name, start_dir=None):
        """method:: new_window(name, [start_dir=None, target=None])
        Creates a new window under the tracked *session*. Updates the tracked
        *session*, *window* and *pane* references.

        :param str name: The name to be applied to the window
        :param start_dir: The starting directory for the new window
        :type start_dir: str or None
        """
        self.session.new_window(name, start_dir=start_dir)

    def select_window(self, index):
        """method:: select_window(index)
        Selects the window with the given index under the tracked *session*.
        Updates the tracked *window* and *pane* references.

        :param str index: The index of the target window
        """
        self.session.select_window(index)

    def next_window(self):
        """method:: next_window()
        Selects the next window under the tracked *session*. Updates the
        tracked *window* and *pane* references.
        """
        self.session.next_window()

    def previous_window(self):
        """method:: previous_window()
        Selects the previous window under the tracked *session*. Updates the
        tracked *window* and *pane* references.
        """
        self.session.previous_window()

    def last_window(self):
        """method:: last_window()
        Selects the last window under the tracked *session*. Updates the
        tracked *window* and *pane* references.
        """
        self.session.last_window()

    def rename_window(self, name):
        """method:: rename_window(name)
        Renames the tracked *window*.

        :param str name: The name to be applied to the window
        """
        self.window.rename(name)

    def kill_window(self):
        """method:: kill_window()
        Kills (removes) the tracked *window* from under the tracked *session*.
        Updates the tracked *session*, *window* and *pane* references.
        """
        self.window.kill()

    def window_split(self, horizontal=False, start_dir=None):
        """method:: window_split([horizontal=False, start_dir=None)
        Splits the tracked *pane*. Updates the tracked *window* and *pane*
        references.

        :param bool horizontal: Defines whether the split is going to be
        vertical (False) or horizontal (True)
        :param start_dir: The starting directory for the new pane
        :type start_dir: str or None
        """
        self.window.split(horizontal, start_dir=start_dir)

    def select_pane(self, index):
        """method:: select_pane(index)
        Selects the pane with the given index under the tracked *window*.
        Updates the tracked *pane* reference.

        :param str index: The index of the target pane
        """
        self.window.select_pane(index)

    def kill_pane(self):
        """method:: kill_pane()
        Kills (removes) the tracked *pane* from under the tracked *window*
        Updates the tracked *window* and *pane* references.
        """
        self.pane.kill()

    def resize_pane(self, width, height):
        """method:: resize_pane(width, height)
        Resizes the tracked *pane* using the given width and height.

        :param str width: The width to be applied to the target pane
        :param str height: The height to be applied to the target pane
        """
        self.pane.resize(width, height)

    def send_keys(self, keys, enter=True):
        """method:: send_keys(keys[, enter=True])
        Sends the given keys to the tracked *pane*.

        :param str keys: The string to be sent to the target pane
        :param bool enter: Defines whether an 'Enter' should be sent after the
        command (True) or not (False)
        """
        self.pane.send_keys(keys, enter)

    def toggle_zoom(self):
        """method:: toggle_zoom()
        Zooms in/out of the tracked *pane*.
        """
        self.pane.zoom()
