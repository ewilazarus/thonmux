class ThonmuxException(Exception):
    pass


class TmuxNotAvailable(ThonmuxException):
    pass


class UnknownCommand(ThonmuxException):
    pass


class UnknownOption(ThonmuxException):
    pass


class EntityNotFound(ThonmuxException):
    pass


class ServerNotFound(EntityNotFound):
    pass


class SessionNotFound(EntityNotFound):
    pass


class WindowNotFound(EntityNotFound):
    pass


class PaneNotFound(EntityNotFound):
    pass


def dispatcher(message):
    e = {
        'unknown command': UnknownCommand,
        'tmux: unknown option': UnknownOption,
        'failed to connect to server': ServerNotFound,
        'session not found': SessionNotFound,
        'window not found': WindowNotFound,
        'can\'t find pane': PaneNotFound,
    }
    for error in e.keys():
        if message.startswith(error):
            raise e[error](message)
    raise ThonmuxException(message)
