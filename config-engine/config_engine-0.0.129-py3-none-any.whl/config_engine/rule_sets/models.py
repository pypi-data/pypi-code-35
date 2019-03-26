from django.db import models
from simple_history.models import HistoricalRecords

from config_engine.base.models import (
    TimeStampedEntity,
    FiniteDurationEntity,
)
from config_engine.payer_source_system.models import CXPayer
from config_engine.semantic_key_registry.models import CXSemanticDataKey, CXSemanticEventKey

COHORT = 'cohort'
GOAL = 'goal'
RECOMMENDATION = 'recommendation'
INFERENCE = 'inference'
AGGREGATION = 'aggregation'
WORKFLOW = 'workflow'
RULE_SET_TYPES = ((COHORT, "cohort"), (GOAL, "goal"), (RECOMMENDATION, "recommendation"),
                  (INFERENCE, "inference"), (AGGREGATION, "aggregation"), (WORKFLOW, "workflow",), )


class Trigger(TimeStampedEntity):
    """
    Event key comes in a zapi msg
    Rule Set name is a key mapped to a Rule Set instance in Config Engine
    """
    payer = models.ForeignKey(CXPayer, on_delete=models.DO_NOTHING)
    semantic_event_key = models.ForeignKey(CXSemanticEventKey,
                                           on_delete=models.DO_NOTHING,
                                           related_name='semantic_event_key_to_trigger')
    history = HistoricalRecords(table_name='simplehistory_trigger')

    class Meta:
        db_table = "cx_trigger"
        unique_together = ("payer", "semantic_event_key")


class TriggerRuleSet(TimeStampedEntity):
    trigger = models.ForeignKey(Trigger, on_delete=models.DO_NOTHING, related_name='trigger_rule_set_to_trigger')
    rule_set = models.ForeignKey('PayerRuleSet',
                                 on_delete=models.DO_NOTHING,
                                 related_name='trigger_to_rule_set')
    history = HistoricalRecords(table_name='simplehistory_trigger_rule_set')

    class Meta:
        db_table = "cx_trigger_rule_set"


class PayerRule(TimeStampedEntity, FiniteDurationEntity):
    """
    When triggered, a `Rule` evaluates a proposition and conditionally
    executes a rule_action if that proposition evaluates to True
    """
    name = models.TextField(null=True, blank=True)
    description = models.TextField()
    payer = models.ForeignKey(CXPayer, on_delete=models.DO_NOTHING)
    prop_chain = models.TextField()
    rule_action = models.ForeignKey('CXRuleAction',
                                    on_delete=models.DO_NOTHING,
                                    related_name='rule_to_rule_action')
    history = HistoricalRecords(table_name='simplehistory_cx_rule')

    class Meta:
        db_table = 'payer_rule'

    def __str__(self):
        return self.name


class PayerRuleSet(TimeStampedEntity, FiniteDurationEntity):
    """ Rulesets are sequenced groups of rules that are executed in a specified order against the same set of data
    """
    name = models.TextField()
    description = models.TextField()
    payer = models.ForeignKey(CXPayer, on_delete=models.DO_NOTHING)
    rule_set_type = models.TextField(null=False, choices=RULE_SET_TYPES)
    pre_process_id = models.TextField()  # TODO: ADD THIS LOGIC, PLACEHOLDER
    post_process_id = models.TextField()  # TODO: ADD THIS LOGIC, PLACEHOLDER
    ordered_rules = models.ManyToManyField(
        PayerRule,
        through='PayerRuleSetRuleSequence',
        through_fields=('rule_set', 'rule'),

        # on_delete=models.CASCADE,
    )
    history = HistoricalRecords(table_name='simplehistory_payer_rule_set')

    class Meta:
        db_table = 'payer_rule_set'

    def __str__(self):
        return self.name


class PayerRuleSetRuleSequence(TimeStampedEntity):
    """  Rules in a set are sequenced by the order in which they are run
    """
    rule_set = models.ForeignKey('PayerRuleSet',
                                 on_delete=models.DO_NOTHING,
                                 related_name='rule_sequence_to_rule_set')
    rule = models.ForeignKey('PayerRule',
                             on_delete=models.DO_NOTHING,
                             related_name='rule_sequence_to_rule')
    sequence = models.IntegerField()
    payer = models.ForeignKey(CXPayer, on_delete=models.DO_NOTHING)
    history = HistoricalRecords(table_name='simplehistory_payer_rule_set_rule_sequence')

    class Meta:
        db_table = 'payer_rule_set_rule_sequence'
        unique_together = ('rule_set', 'rule')


class CXProposition(TimeStampedEntity):
    """ A 'proposition' is a statement consisting of a subject and a predicate
    that may either be true or false.  Here, `argument` forms the subject and
    the `operator` and `predicate_val` (or `predicate_sk`) form the predicate
    """
    OPERATORS = (
        ('==', 'equal to'),
        ('!=', 'not equal to'),
        ('is', 'is'),
        ('is not', 'is not'),
        ('>', 'greater than'),
        ('>=', 'greater than or equal to'),
        ('<', 'less than'),
        ('<=', 'less than or equal to'),
        ('in', 'in'),
        ('not in', 'not in')
    )
    argument_attribute = models.ForeignKey(
        CXSemanticDataKey, on_delete=models.DO_NOTHING, null=False, related_name='proposition_to_semantic_data_key')
    operator = models.TextField(null=False, choices=OPERATORS)
    predicate_val = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'cx_proposition'

    def __str__(self):
        val = "[?? UNKNOWN VAL ??]"
        if self.predicate_val:
            val = self.predicate_val
        # elif self.predicate_sk:
        #     val = "[result of '{}']".format(self.predicate_sk.internal_display_name)
        return "({arg} {op} {val})".format(arg=self.argument_attribute.display_name,
                                           op=self.operator,
                                           val=val)


class CXRuleAction(TimeStampedEntity):
    display_name = models.TextField(unique=True)
    description = models.TextField()
    rule_action_type = models.TextField(null=False, choices=RULE_SET_TYPES)

    class Meta:
        db_table = 'cx_rule_action'
