.. thonmux documentation master file, created by
   sphinx-quickstart on Mon Jun  8 10:57:42 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to thonmux's documentation!
===================================

The thonmux library was designed to be an API to tmux and enable one to 
interact with it programatically, using Python, in a pythonic way.

Get to know `the code`_.

.. _`the code`: thonmux.html

How it works
------------

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
    >>> t.window_split()
    >>> t.pane
    Pane(index=1, dimensions=[159x20], active=True)
    >>> t.send_keys('ls -la | grep .py')
    ...

Installation
------------

TODO

FAQ
---

1. Why use thonmux?

   * thonmux makes things pythonic.

2. Why not use something else, like tmuxp?

   * tmuxp is a good project but sometimes it doesn't attend to my
     expectations.

3. How can I help?

   * https://github.com/ewilazarus/thonmux


Contents:

.. toctree::
   :maxdepth: 2

   thonmux

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

