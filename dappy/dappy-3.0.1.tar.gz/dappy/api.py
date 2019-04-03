from dappy.endpoint import CompleteEndpoint
from dappy.formatters import default_formatter

# Represents an API and all of its endpoints
class API:

    def __init__(self, netloc, endpoints, scheme='https', formatter=default_formatter):
        for endpoint in endpoints:
            # This allows us to do things like API.endpoint.get(...)
            setattr(
                self,
                endpoint.name,
                CompleteEndpoint(
                    scheme,
                    netloc,
                    endpoint,
                    formatter=formatter if endpoint.formatter is None else endpoint.formatter
                )
            )