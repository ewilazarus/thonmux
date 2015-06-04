class TmuxNotAvailable(Exception):
    pass


class UnknownCommand(Exception):
    pass


class UnknownOption(Exception):
    pass


class ObjectNotFound(Exception):
    pass


class ServerNotFound(ObjectNotFound):
    pass


class SessionNotFound(ObjectNotFound):
    pass


class WindowNotFound(ObjectNotFound):
    pass


class PaneNotFound(ObjectNotFound):
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
