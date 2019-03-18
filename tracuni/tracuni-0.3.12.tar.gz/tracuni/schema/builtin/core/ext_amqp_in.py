import json
from functools import partial

from tracuni.define.type import (
    Rule,
    Destination,
    DestinationSection,
    Origin,
    OriginSection,
    Stage,
    PipeCommand,
)
from tracuni.schema.pipe_methods import (
    ext_tracer_out_point,
    pipe_head,
    pipe_sep_string,
    pipe_mask_secret_catch_essentials,
    pipe_dump,
    pipe_cut,
    ext_api_kind,
)


def deb(x):
    return x


ruleset = (
    Rule(
        description="Сохранить тело сообщения",
        destination=Destination(DestinationSection.REUSE, 'message'),
        pipeline=(
            pipe_head,
            lambda data: json.loads(data.decode()),
        ),
        origins=(
            Origin(
                OriginSection.POINT_ARGS, "body",
            ),
        ),
        stage=Stage.INIT,
    ),
    Rule(
        description="Сохранить заголовки сообщения",
        destination=Destination(DestinationSection.REUSE, 'message_properties'),
        pipeline=(
            pipe_head,
        ),
        origins=(
            Origin(
                OriginSection.POINT_ARGS, "properties",
            ),
        ),
        stage=Stage.INIT,
    ),
    Rule(
        description="Сохранить конверт сообщения",
        destination=Destination(DestinationSection.REUSE, 'message_envelope'),
        pipeline=(
            pipe_head,
        ),
        origins=(
            Origin(
                OriginSection.POINT_ARGS, "envelope",
            ),
        ),
        stage=Stage.INIT,
    ),
    Rule(
        description="Разместить заголовки контекста трассера там, "
                    "где фабрика участков их ищет",
        destination=Destination(DestinationSection.REUSE, 'tracer_headers'),
        pipeline=(
            pipe_head,
            lambda x: dict((k.lower(), v) for k, v in (x or {}).items()),
        ),
        origins=(
            Origin(
                OriginSection.REUSE,
                lambda data: data['message_properties'].headers,
            ),
        ),
        stage=Stage.INIT,
    ),
    Rule(
        description="Разместить заголовки контекста трассера там, "
                    "где фабрика участков их ищет (из тела сообщения)",
        destination=Destination(DestinationSection.REUSE, 'tracer_headers'),
        pipeline=(
            pipe_head,
            lambda x: dict((k.lower(), v) for k, v in (x or {}).items()),
        ),
        origins=(
            Origin(
                OriginSection.REUSE,
                lambda data: data['message'].get('context_headers'),
            ),
        ),
        stage=Stage.INIT,
    ),


    # Rule(
    #     description="Наименование AMQP exchange сохранить для "
    #                 "переиспользования",
    #     destination=Destination(
    #         DestinationSection.REUSE,
    #         'amqp_exchange',
    #     ),
    #     pipeline=(
    #         pipe_head,
    #         lambda v: v.exchange_name,
    #     ),
    #     origins=(
    #         Origin(OriginSection.POINT_ARGS, 'envelope'),
    #     ),
    #     stage=Stage.INIT,
    # ),
    Rule(
        description="Задать имя участку",
        destination=Destination(
            DestinationSection.SPAN_NAME,
            'name'
        ),
        pipeline=(
            deb,
            lambda x: ("amqp", x[0].lower(), x[1]),
            partial(pipe_sep_string, **{'sep': ('::', ' (', ')')}),
        ),
        origins=(
            Origin(
                OriginSection.REUSE,
                lambda data: data['message'].get('method', ''),
            ),
            Origin(
                OriginSection.REUSE,
                lambda data: data['message_envelope'].exchange_name,
            ),
        ),
        stage=Stage.PRE,
    ),
    # Rule(
    #     description="Задать имя участку",
    #     destination=Destination(
    #         DestinationSection.SPAN_NAME,
    #         'name'
    #     ),
    #     pipeline=(
    #         partial(pipe_sep_string, **{'sep': ("::", " (", ")")}),
    #     ),
    #     origins=(
    #         Origin(
    #             OriginSection.ENGINE,
    #             ext_api_kind,
    #         ),
    #         Origin(
    #             OriginSection.REUSE,
    #             "peer_name",
    #         ),
    #         Origin(
    #             OriginSection.CALL_STACK,
    #             partial(ext_tracer_out_point, **{"shift": 0}),
    #         ),
    #     ),
    #     stage=Stage.INIT,
    # ),
    # Rule(
    #     description="Наименование партнерского сервиса записать в участок",
    #     destination=Destination(
    #         DestinationSection.SPAN_NAME,
    #         'remote_endpoint',
    #     ),
    #     pipeline=(
    #         pipe_head,
    #     ),
    #     origins=(
    #         Origin(OriginSection.REUSE, 'peer_name'),
    #     ),
    #     stage=Stage.PRE,
    # ),
    Rule(
        description="Задать имя партнёрской точки для участка",
        destination=Destination(
            DestinationSection.SPAN_NAME,
            'remote_endpoint',
        ),
        pipeline=(
            pipe_head,
        ),
        origins=(
            Origin(
                OriginSection.REUSE,
                lambda data: data.get('tracer_headers', {}).get('x-b3-servicename', ''),
            ),

        ),
        stage=Stage.PRE,
    ),
    Rule(
        description="Вывести тело сообщения в аннотации",
        destination=Destination(DestinationSection.SPAN_LOGS, 'message'),
        pipeline=(
            pipe_head,
            # pipe_catch_essential,
            pipe_dump,
            pipe_cut,
            pipe_mask_secret_catch_essentials,
            lambda x: x[1],
            PipeCommand.TEE,
            Destination(DestinationSection.SPAN_TAGS, {}),
            pipe_head,
        ),
        origins=(
            Origin(
                OriginSection.REUSE, "message",
            ),
        ),
        stage=Stage.PRE,
    ),
    # Rule(
    #     description="Запомнить ошибку для вывода",
    #     destination=Destination(DestinationSection.REUSE, 'error'),
    #     pipeline=(
    #         pipe_head,
    #     ),
    #     origins=(
    #         Origin(OriginSection.SPAN, 'error'),
    #     ),
    #     stage=Stage.POST,
    # ),
)
