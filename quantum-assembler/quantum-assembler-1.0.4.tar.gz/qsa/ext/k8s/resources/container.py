

class Container:

    @property
    def args(self):
        return self.spec.setdefault('args', [])

    @property
    def env(self):
        return self.spec.setdefault('env', [])

    def __init__(self, spec):
        self.spec = spec

    def setargs(self, value):
        """Set the arguments of the container."""
        self.spec.args = value
        return self

    def setenv(self, key, value):
        """Set an environment variable in the container."""
        self.env.append({'name': key, 'value': value})
        return self
