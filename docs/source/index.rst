.. thonmux documentation master file, created by
   sphinx-quickstart on Mon Jun  8 10:57:42 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to thonmux's documentation!
===================================

.. note:: This package is not Python 2.x compatible.

The thonmux library was designed to be a Python API to *interact with tmux in a pythonic way*.

Supported commands
------------------

* kill-pane - :meth:`thonmux.Thonmux.kill_pane`
* kill-window - :meth:`thonmux.Thonmux.kill_window`
* last-window - :meth:`thonmux.Thonmux.last_window`
* new-window - :meth:`thonmux.Thonmux.new_window`
* next-window - :meth:`thonmux.Thonmux.next_window`
* previous-window - :meth:`thonmux.Thonmux.previous_window`
* rename-session - :meth:`thonmux.Thonmux.rename_session`
* rename-window - :meth:`thonmux.Thonmux.rename_window`
* resize-pane - :meth:`thonmux.Thonmux.resize_pane`
* select-pane - :meth:`thonmux.Thonmux.select_pane`
* select-window - :meth:`thonmux.Thonmux.select_window`
* send-keys - :meth:`thonmux.Thonmux.send_keys`
* split-window - :meth:`thonmux.Thonmux.split_window`

There's also a few convenience commands:

* toggle-zoom - :meth:`thonmux.Thonmux.toggle_zoom` (zooms in/out of the
    tracked pane)
* next-pane - :meth:`thonmux.Thonmux.next_pane` (selects the next pane under
    the tracked window)
* previous-pane - :meth:`thonmux.Thonmux.previous_pane` (selects the previous
    pane under the tracked window)

Quickstart
----------

    >>> from thonmux import Thonmux
    >>> t = Thonmux('new-session')
    >>> t
    Thonmux[Session(name=new-session, creation=2015-06-07 18:43:20, attached=False), Window(index=0, name=zsh, dimensions=[159x42], active=True), Pane(index=0, dimensions=[159x42], active=True)]
    >>> t.new_window('new-window')
    >>> t
    Thonmux[Session(name=new-session, creation=2015-06-07 18:43:20, attached=False), Window(index=1, name=new-window, dimensions=[159x42], active=True), Pane(index=0, dimensions=[159x42], active=True)]
    >>> t.session.windows
    [Window(index=0, name=zsh, dimensions=[159x42], active=False), Window(index=1, name=new-window, dimensions=[159x42], active=True)]
    >>> t.window
    Window(index=1, name=new-window, dimensions=[159x42], active=True)
    >>> t.rename_window('renamed-window')
    >>> t.window
    Window(index=1, name=renamed-window, dimensions=[159x42], active=True)
    >>> t.session.windows
    [Window(index=0, name=zsh, dimensions=[159x42], active=False), Window(index=1, name=renamed-window, dimensions=[159x42], active=True)]
    >>> t.split_window()
    >>> t.pane
    Pane(index=1, dimensions=[159x20], active=True)
    >>> t.send_keys('ls -la | grep .py')
    ...

Installation
------------
::

   $ pip install thonmux

FAQ
---

1. Why use thonmux?

   * thonmux makes things pythonic.

2. Why not use something else, like tmuxp?

   * tmuxp is a good project but sometimes it doesn't attend to my
     expectations.

3. How can I help?

   * https://github.com/ewilazarus/thonmux

4. I found a bug, what do I do?

   * Please notify it at https://github.com/ewilazarus/thonmux/issues

Contents:

.. toctree::
   :maxdepth: 2

   self
   thonmux

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

