thonmux
=======

API for interaction with tmux in a pythonic way.

#How it works

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
