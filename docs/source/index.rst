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

    >>> from thonmux import Server, Manager
    >>> server = Server()
    >>> server.sessions
    [Session(name=0, creation=2015-06-06 12:55:21, attached=False)]
    >>> server.new_session('new-session')
    >>> server.sessions
    [Session(name=0, creation=2015-06-06 12:55:21, attached=False), Session(name=new-session, creation=2015-06-06 16:57:30, attached=False)]
    >>> session = server.find_session('new-session')
    >>> session
    Session(name=new-session, creation=2015-06-06 16:57:30, attached=False)
    >>> m = Manager(session)
    >>> m
    Manager[session=Session(name=new-session, creation=2015-06-06 16:57:30, attached=False), window=Window(index=0, name=zsh, dimensions=[80x23], active=True, pane=Pane(index=0, dimensions=[80x23], active=True)]
    >>> m.new_window('new-window')
    >>> m
    Manager[session=Session(name=new-session, creation=2015-06-06 16:57:30, attached=False), window=Window(index=1, name=new-window, dimensions=[80x23], active=True, pane=Pane(index=0, dimensions=[80x23], active=True)]
    >>> m.session.windows
    [Window(index=0, name=zsh, dimensions=[80x23], active=False), Window(index=1, name=new-window, dimensions=[80x23], active=True)]
    >>> m.window.panes
    [Pane(index=0, dimensions=[80x23], active=True)]
    >>> m.window_split()
    >>> m.window.panes
    [Pane(index=0, dimensions=[80x11], active=False), Pane(index=1, dimensions=[80x11], active=True)]
    m.send_keys('echo $HOME')

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

