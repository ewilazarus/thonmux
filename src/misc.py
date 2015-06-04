def instance_factory(cls, parser, parent, output):
    instances = []
    for line in output:
        kwargs = parser(line)
        instances.append(cls(parent, **kwargs))
    return instances
