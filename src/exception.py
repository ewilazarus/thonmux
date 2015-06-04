class TmuxNotAvailable(Exception):
    pass


class UnknownCommand(Exception):
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


def dispatcher(error):
    e = {
        'unknown command': UnknownCommand,
        'failed to connect to server': ServerNotFound,
        'session not found': SessionNotFound,
        'window not found': WindowNotFound,
        'can\'t find pane': PaneNotFound,
    }
    for message in e.keys():
        if error.startswith(message):
            raise e[message]()
