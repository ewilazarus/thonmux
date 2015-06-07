.. Thonmux documentation master file, created by
   sphinx-quickstart on Sat Jun  6 16:36:14 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Thonmux's documentation!
===================================

Thonmux is a library designed to provide python interfaces for interacting with
tmux.

-------------------------------------------------------------------------------

How to use Thonmux:

    >>> from thonmux import Thonmux
    >>> t = Thonmux('my-session')
    >>> t
    Thonmux[Session(name=my-session, creation=2015-06-07 10:58:16, attached=False), Window(index=0, name=zsh, dimensions=[80x23], active=True), Pane(index=0, dimensions=[80x23], active=True)]
    >>> t.new_window('new-window')
    >>> t
    Thonmux[Session(name=my-session, creation=2015-06-07 10:58:16, attached=False), Window(index=1, name=new-window, dimensions=[80x23], active=True), Pane(index=0, dimensions=[80x23], active=True)]
    >>> t.session.windows
    [Window(index=0, name=zsh, dimensions=[80x23], active=False), Window(index=1, name=new-window, dimensions=[80x23], active=True)]
    >>> t.window.panes
    [Pane(index=0, dimensions=[80x23], active=True)]
    >>> t.window_split()
    >>> t.window.panes
    [Pane(index=0, dimensions=[80x11], active=False), Pane(index=1, dimensions=[80x11], active=True)]
    >>> t.send_keys('echo $HOME')
    ...

-------------------------------------------------------------------------------

Questions:

1. Why Thonmux?
   * There are other libraries/solutions out there built to interact with tmux, but most of them either don't use python or are not straight forward (pythonic).
2. Why/where should I use it?
   * You could use it to make all kinds of crazy configurations to your tmux environments such as to set them up programatically.
3. Why not use something more solid like 'tmuxp' or even 'tmuxinator'?
   * Tmuxp is a good project and I used it myself before starting the Thonmux project, but I needed something simpler. Tmuxinator? Also a good project but I don't really want to install ruby.
4. How can I help?
   * Send a pull request to http://github.com/ewilazarus/thonmux




.. toctree::
   :maxdepth: 2


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

