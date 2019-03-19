from attr import attrs, attrib


@attrs
class Requirements(object):
    dependencies = attrib()


@attrs
class ClientContext(object):
    custom = attrib()
    env = attrib(default=None)
    client = attrib(default=None)


@attrs
class LambdaFunction(object):
    app_name = attrib()
    stage = attrib()
    function_name = attrib()
    handler = attrib()
    tags = attrib()
    filename = attrib()
    runtime = attrib()
    timeout = attrib()
    memory_size = attrib()
    role = attrib(default=None)
    security_group_ids = attrib(default=None)
    subnet_ids = attrib(default=None)
    environment = attrib(default=None)
