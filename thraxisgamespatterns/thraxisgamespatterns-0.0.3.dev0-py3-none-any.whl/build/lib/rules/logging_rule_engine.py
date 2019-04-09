# package com.games.thraxis.framework.rules;
#
# import com.games.thraxis.framework.logging.TGLogger;
#
# /**
#  * Created by Zack on 10/2/2017.
#  */
#
# public class TGLoggingRuleEngine extends TGBaseRuleEngine {
#
# 	private final String format;
# 	private final TGLogger logger;
#
# 	public TGLoggingRuleEngine(TGLogger logger, String format) {
# 		this.logger = logger;
# 		this.format = format;
# 	}
#
# 	public TGLoggingRuleEngine(TGLogger logger) {
# 		this(logger, "Applying Rule: %s");
# 	}
#
# 	@Override
# 	protected <C> void applyRule(TGRuleCore<C> rule, C context) {
# 		logRuleApplied(rule, context);
# 		super.applyRule(rule, context);
# 	}
#
# 	protected <C> void logRuleApplied(TGRuleCore<C> rule, C context) {
# 		logger.info(getClass(), format, rule);
# 	}
# }
from rules.rule_engine import TGBaseRuleEngine


class TGLoggingRuleEngine(TGBaseRuleEngine):
    def __init__(self, logger, formatting="Applying Rule: {}"):
        self.logger = logger
        self.formatting = formatting

    def apply_rule(self, rule, context):
        self.log_rule_applied(rule)
        super().apply_rule(rule, context)

    def log_rule_applied(self, rule):
        self.logger.info(self.formatting, rule)
