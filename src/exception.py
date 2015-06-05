import logging

logger = logging.getLogger(__name__)


class MysteriousException(Exception):
    pass


class TmuxNotAvailable(Exception):
    pass


class UnknownCommand(Exception):
    pass


class UnknownOption(Exception):
    pass


class EntityOutOfSync(Exception):
    pass


class CreateWindowFailed(EntityOutOfSync):
    pass


class ServerNotFound(EntityOutOfSync):
    pass


class SessionNotFound(EntityOutOfSync):
    pass


class WindowNotFound(EntityOutOfSync):
    pass


class PaneNotFound(EntityOutOfSync):
    pass


def dispatcher(message):
    e = {
        'unknown command': UnknownCommand,
        'tmux: unknown option': UnknownOption,
        'failed to connect to server': ServerNotFound,
        'session not found': SessionNotFound,
        'window not found': WindowNotFound,
        'can\'t find pane': PaneNotFound,
        'create window failed': CreateWindowFailed,
    }
    for error in e.keys():
        if message.startswith(error):
            raise e[error](message)
    logger.error(('Please, check if this exception has already been notified,'
                  ' otherwise notify it at'
                  ' https://github.com/ewilazarus/thonmux/issues'))
    raise MysteriousException(message)
