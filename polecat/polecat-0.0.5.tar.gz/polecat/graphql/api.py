from graphql_server import (default_format_error, encode_execution_results,
                            run_http_query)

from .schema import make_graphql_schema


class GraphqlAPI:
    def prepare(self):
        self.schema = make_graphql_schema()

    async def handle_event(self, event):
        if not event.is_http() or event.request.path != '/graphql':
            return None
        # TODO: There's no sync version of this for some reason...
        result = await run_http_query(
            self.schema,
            event.request.method.lower(),
            event.request.json,
            # query_data=None,
            # batch_enabled=False,
            # catch=False
        )
        is_batch = False  # TODO: How to handle this?
        result = encode_execution_results(
            result[0],
            default_format_error,
            is_batch,
            lambda d: d  # pass-through
        )
        return result
