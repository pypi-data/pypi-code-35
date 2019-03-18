#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Привязка наборов правил к вариантам

    variant => ruleset

    ruleset = (
        Rule(
            description='',
            destination=Destination(
                section=DestinationSection.SPAN_TAGS,
                name='some'
            ),
            stage=Stage.PRE,
            origins=(
                Origin(section=OriginSection.REUSE, getter='some'),
            ),
            pipeline=(lambda x: x,),
        ),
    )  # type: RuleSet
"""
from functools import partial
from typing import TYPE_CHECKING

from tracuni.misc.select_coroutine import is_tornado_on
from tracuni.define.type import (
    Variant,
    SpanSide,
    APIKind,
    Rule,
    Destination,
    DestinationSection,
    PipeCommand,
    Origin,
    OriginSection,
    Stage,
)
from tracuni.schema.pipe_methods import (
    pipe_head,
    pipe_inject_headers,
    ext_out_headers,
)

if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences
    from ..define.type import RuleSet  # noqa
    from ..define.type import Schema  # noqa

####################
# Подключение стандартных настроек экстракторов

# для варианта будет использован только один из наборов для определённого
# ключа назначения в зависимости от разновидности ключа экстракторы
# применяются в следующем приоритете сверху вниз (если применяется верхний,
# то нижний уже не применяется)
#  - элементы с конкретным вариантом применяются
# только для этого варианта
#  - элементы привязанные только к направлению применяются ко всем вариантам
#  с этим направлением
#  - элементы привязанные по виду API применяются ко всем вариантам с этим
#  видом
#  - непривязанные к вариантам элементы применяются ко всем вариантам


def get_standard_schema():
    if is_tornado_on():
        from tracuni.schema.builtin import (
            tornado_http_in_ruleset as http_in_ruleset,
            tornado_http_out_ruleset as http_out_ruleset,
            tornado_db_out_ruleset as db_out_ruleset,
            tornado_amqp_out_ruleset as amqp_out_ruleset,
            amqp_in_ruleset,
        )
    else:
        from tracuni.schema.builtin import (
            http_in_ruleset,
            http_out_ruleset,
            amqp_in_ruleset,
            amqp_out_ruleset,
            db_out_ruleset,
        )
    standard_schema = {
        Variant(SpanSide.IN, APIKind.HTTP): http_in_ruleset,
        Variant(SpanSide.OUT, APIKind.HTTP): http_out_ruleset,
        Variant(SpanSide.IN, APIKind.AMQP): amqp_in_ruleset,
        Variant(SpanSide.OUT, APIKind.AMQP): amqp_out_ruleset,
        Variant(SpanSide.OUT, APIKind.DB): db_out_ruleset,
    }  # type: Schema
    return standard_schema


rule_amqp_out_tracer_context = Rule(
        description="Записать X-B3- заголовки в заголовки сообщения",
        destination=Destination(DestinationSection.POINT_ARGS, 'properties'),
        pipeline=(
            lambda data: (data[:3], data[3]),
            lambda data: (data[0], getattr(data[1], 'context_amqp_name', None)),
            # lambda data: pipe_inject_headers(data[0], data[1]) if data[1] else None,
            # PipeCommand.TEE,
            # Destination(DestinationSection.POINT_ARGS, 'message'),
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
