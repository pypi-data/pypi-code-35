from .site import site_metadata_rules


class MetadataRuleEvaluator:

    """Main class to evaluate rules.

    Used by model mixin.
    """

    def __init__(self, visit=None, app_label=None):
        self.visit = visit
        self.app_label = app_label or visit._meta.app_label

    def evaluate_rules(self):
        for rule_group in site_metadata_rules.registry.get(self.app_label, []):
            rule_group.evaluate_rules(visit=self.visit)
