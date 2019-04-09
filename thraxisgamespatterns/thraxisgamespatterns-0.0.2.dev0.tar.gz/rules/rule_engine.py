# package com.games.thraxis.framework.rules;
#
# import java.util.Collection;
#
# /##
#  # Lightweight system for evaluating conditional behavior
#  #/
#
# public class TGBaseRuleEngine implements TGRuleEngine {
#
# 	public static final TGBaseRuleEngine DEFAULT = new TGBaseRuleEngine();
# 	protected static final Void NOTHING = null;
#
# 	@Override
# 	public <C, R extends TGRuleCore<C>> void applyAll(Collection<R> rules, C context) {
# 		for (TGRuleCore<C> rule : rules) {
# 			considerApplying(context, rule);
# 		}
# 	}
#
# 	@Override
# 	public <R extends TGRuleCore<Void>> void applyAll(Collection<R> rules) {
# 		applyAll(rules, NOTHING);
# 	}
#
# 	@Override
# 	public <R extends TGRuleCore<Void>> void applyFirst(Collection<R> rules) {
# 		applyFirst(rules, NOTHING);
# 	}
#
# 	@Override
# 	public <C, R extends TGRuleCore<C>> void applyFirst(Collection<R> rules, C context) {
#
# 		for (TGRuleCore<C> rule : rules) {
# 			if (rule.isApplicable(context)) {
# 				applyRule(rule, context);
# 				return;
# 			}
# 		}
# 	}
#
# 	protected <C> void applyRule(TGRuleCore<C> rule, C context) {
# 		rule.applyTo(context);
# 	}
#
# 	protected <C> void considerApplying(C context, TGRuleCore<C> rule) {
# 		if (rule.isApplicable(context)) {
# 			applyRule(rule, context);
# 		}
# 	}
# }


class TGBaseRuleEngine:

    def apply_all(self, rules, context=None):
        for rule in rules:
            self.consider_applying(context, rule)

    def apply_first(self, rules, context=None):
        for rule in rules:
            if rule.is_applicable(context):
                self.apply_rule(rule, context)
                return

    @staticmethod
    def apply_rule(rule, context):
        rule.apply_to(context)

    def consider_applying(self, context, rule):
        if rule.is_applicable(context):
            self.apply_rule(rule, context)


DEFAULT = TGBaseRuleEngine()
