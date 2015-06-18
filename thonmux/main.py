# -*- coding: utf-8 -*-
import logging

from .misc import synchronous
from .server import Server

logger = logging.getLogger(__name__)


@synchronous
class Thonmux:
    """The tmux interface

    This class prevents that interactions with tmux result in an out of
    sync entity tree, where the python objects representation differ from what
    really exists in tmux.

    It works by keeping track of the *session* provided to its constructor, as
    well as to its active *window* and active *pane*. Whenever an action that
    would alter the tree's state happens, it raises an
    :class:`exception.EntityOutOfSync` that is handled by reconstructing the
    tree and updating the references of the tracked *session*, *window* and
    *pane*.

    All tmux commands are run against the tracked *session*, *window* and
    *pane* as needed.

    :param str session_name: The name of target session. If a session with the
        provided name already exists, it will attach to it. Otherwise, it will
        create a new session with the provided name
    :param str socket_name: The name of the socket to be used to localize the
        tmux server
    :param socket_path: The path of the socket to be used to localize the
        tmux server
    :type socket_path: str or None

    :ivar session: the tracked *session*
    :vartype session: :class:`Session`
    :ivar window: the tracked *window*
    :vartype window: :class:`Window`
    :ivar pane: the tracked *pane*
    :vartype pane: :class:`Pane`
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
        """Renames the tracked *session*

        :param str name: The name to be applied to the session
        """
        self.session.rename(name)

    def new_window(self, name, start_dir=None):
        """Creates a new window under the tracked *session*. Updates the
        tracked *session*, *window* and *pane* references

        :param str name: The name to be applied to the window
        :param start_dir: The starting directory for the new window
        :type start_dir: str or None
        """
        self.session.new_window(name, start_dir=start_dir)

    def select_window(self, index):
        """Selects the window with the given index under the tracked *session*.
        Updates the tracked *window* and *pane* references

        :param str index: The index of the target window
        """
        self.session.select_window(index)

    def next_window(self):
        """Selects the next window under the tracked *session*. Updates the
        tracked *window* and *pane* references
        """
        self.session.next_window()

    def previous_window(self):
        """Selects the previous window under the tracked *session*. Updates the
        tracked *window* and *pane* references
        """
        self.session.previous_window()

    def last_window(self):
        """Selects the last window under the tracked *session*. Updates the
        tracked *window* and *pane* references
        """
        self.session.last_window()

    def rename_window(self, name):
        """Renames the tracked *window*

        :param str name: The name to be applied to the window
        """
        self.window.rename(name)

    def kill_window(self):
        """Kills (removes) the tracked *window* from under the tracked
        *session*. Updates the tracked *session*, *window* and *pane*
        references
        """
        self.window.kill()

    def split_window(self, horizontal=False, start_dir=None):
        """Splits the tracked *pane*. Updates the tracked *window* and *pane*
        references

        :param bool horizontal: Defines whether the split is going to be
            vertical (False) or horizontal (True)
        :param start_dir: The starting directory for the new pane
        :type start_dir: str or None
        """
        self.window.split(horizontal, start_dir=start_dir)

    def select_pane(self, index):
        """Selects the pane with the given index under the tracked *window*.
        Updates the tracked *pane* reference

        :param str index: The index of the target pane
        """
        self.window.select_pane(index)

    def next_pane(self):
        """Selects the next pane under the tracked *window*. Updates the
        tracked *pane* reference
        """
        self.pane.next()

    def previous_pane(self):
        """Selects the previous pane under the tracked *window*. Updates the
        tracked *pane* reference
        """
        self.pane.previous()

    def kill_pane(self):
        """Kills (removes) the tracked *pane* from under the tracked *window*
        Updates the tracked *window* and *pane* references
        """
        self.pane.kill()

    def resize_pane(self, width, height):
        """Resizes the tracked *pane* using the given width and height

        :param str width: The width to be applied to the target pane
        :param str height: The height to be applied to the target pane
        """
        self.pane.resize(width, height)

    def send_keys(self, keys, enter=True):
        """Sends the given keys to the tracked *pane*

        :param str keys: The string to be sent to the target pane
        :param bool enter: Defines whether an 'Enter' should be sent after the
            command (True) or not (False)
        """
        self.pane.send_keys(keys, enter)

    def toggle_zoom(self):
        """Zooms in/out of the tracked *pane*
        """
        self.pane.zoom()
