import inspect
import types
from functools import wraps
import logging

from . import exception

logger = logging.getLogger(__name__)


def instance_factory(cls, parser, parent, output):
    logger.debug('Creating %d %s\'s instance(s)' % (len(output), cls.__name__))
    instances = []
    for line in output:
        kwargs = parser(line)
        logger.debug('parsed kwargs: ' + str(kwargs))
        instances.append(cls(parent, **kwargs))
    return instances


def synchronous(cls):
    def action(f):
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            try:
                return f(self, *args, **kwargs)
            except exception.EntityOutOfSync:
                self._sync()
            except exception.EntityNotFound:
                # TODO
                raise NotImplementedError('entity might not be up to date')
        return wrapper

    for name, member in inspect.getmembers(cls):
        if isinstance(member, types.FunctionType):
            setattr(cls, name, action(member))
    return cls
