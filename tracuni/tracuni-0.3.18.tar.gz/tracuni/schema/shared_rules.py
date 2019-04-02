from functools import partial

from tracuni.define.type import Rule, Destination, DestinationSection, Origin, OriginSection, Stage
from tracuni.schema.pipe_methods import pipe_head, pipe_inject_headers, ext_out_headers

rule_amqp_out_tracer_context = Rule(
        description="Записать X-B3- заголовки в заголовки сообщения",
        destination=Destination(DestinationSection.POINT_ARGS, 'properties'),
        pipeline=(
            lambda data: (data[:3], data[3]),
            lambda data: (data[0], getattr(data[1], 'context_amqp_name', None)),
            pipe_head,
            partial(pipe_inject_headers, **{'prefix_key': 'headers'}),
        ),
        origins=(
            Origin(
                OriginSection.SPAN, None,
            ),
            Origin(
                OriginSection.POINT_ARGS, ext_out_headers,
            ),
            Origin(
                OriginSection.ADAPTER,
                lambda adapter: adapter.config.service_name,
            ),
            Origin(OriginSection.ADAPTER, "config",),
        ),
        stage=Stage.PRE,
    )
