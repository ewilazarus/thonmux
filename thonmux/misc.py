import logging

logger = logging.getLogger(__name__)


def instance_factory(cls, parser, parent, output):
    logger.debug('Creating %d %s\'s instance(s)' % (len(output), cls.__name__))
    instances = []
    for line in output:
        kwargs = parser(line)
        logger.debug('parsed kwargs: ' + str(kwargs))
        instances.append(cls(parent, **kwargs))
    return instances
