thonmux
=======

API for interaction with tmux in a pythonic way.

###How it works

    >>> from thonmux import Thonmux
    >>> t = Thonmux()
    >>> t.new_session('new-session', dettached=False)
    >>> t.session
	Session(name=new-session, creation=2015-06-07 18:43:20, attached=True)
    >>> t.new_window('new-window')
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

###Documentation

http://thonmux.readthedocs.org/en/latest/index.html
