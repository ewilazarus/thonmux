import logging

logger = logging.getLogger(__name__)


class MysteriousException(Exception):
    pass


class TmuxNotAvailable(Exception):
    pass


class IllegalCommand(Exception):
    pass


class EntityOutOfSync(Exception):
    pass


class EntityNotFound(Exception):
    pass


def dispatcher(message):
    e = {
        'unknown command': IllegalCommand,
        'tmux: unknown option': IllegalCommand,
        'create window failed': IllegalCommand,
        'failed to connect to server': EntityNotFound,
        'session not found': EntityNotFound,
        'window not found': EntityNotFound,
        'can\'t find pane': EntityNotFound,
    }
    for error in e.keys():
        if message.startswith(error):
            raise e[error](message)
    logger.error(('Please, check if this exception has already been notified,'
                  ' otherwise notify it at'
                  ' https://github.com/ewilazarus/thonmux/issues'))
    raise MysteriousException(message)
