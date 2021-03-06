import logging

logger = logging.getLogger(__name__)


class MysteriousException(Exception):
    """
    Raised whenever all the other exceptions declared in this package are not
    triggered
    """
    pass


class TmuxNotAvailable(Exception):
    """
    Raised when the tmux executable is either not found or not accessible
    """
    pass


class IllegalCommand(Exception):
    """
    Raised when trying to run an unknown or bad-composed command
    """
    pass


class EntityOutOfSync(Exception):
    """
    Raised whenever an action changes the tmux entities' structure tree
    """
    pass


class EntityNotFound(Exception):
    """
    Raised when trying to execute a command targeting a missing tmux entity
    """
    pass


class SessionDoesNotExist(Exception):
    """
    Raised whenever the client tries to attach to a session that does not exist
    under the current server
    """
    pass

class SessionAlreadyExists(Exception):
    """
    Raised whenever the client tries to create a session with a duplicated name
    """
    pass

class NestedSessions(Exception):
    """
    Raised whenever the client tries to create a session within another session
    """

def dispatcher(message):
    e = {
        'unknown command': IllegalCommand,
        'tmux: unknown option': IllegalCommand,
        'create window failed': IllegalCommand,
        'failed to connect to server': EntityNotFound,
        'session not found': EntityNotFound,
        'window not found': EntityNotFound,
        'can\'t find pane': EntityNotFound,
        'duplicate session': SessionAlreadyExists,
        'sessions should be nested with care': NestedSessions,
    }
    for error in e.keys():
        if message.startswith(error):
            raise e[error](message)
    raise MysteriousException(message)
    logger.error(('Please, check if this exception has already been notified,'
                  ' otherwise notify it at'
                  ' https://github.com/ewilazarus/thonmux/issues'))
