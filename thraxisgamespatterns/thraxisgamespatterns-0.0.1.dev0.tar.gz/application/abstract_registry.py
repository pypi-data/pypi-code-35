# package com.games.thraxis.framework.application;
#
# import java.util.Map;
#
# import android.content.Context;
#
# import com.games.thraxis.engine.game.TGGame;
# import com.games.thraxis.framework.assertions.TGBaseWatchDog;
# import com.games.thraxis.framework.assertions.TGWatchDog;
# import com.games.thraxis.framework.eventhandling.TGEventDistributor;
# import com.games.thraxis.framework.eventhandling.TGEventTracker;
# import com.games.thraxis.framework.eventhandling.TGPublisher;
# import com.games.thraxis.framework.eventhandling.TGSynchronizedEventTracker;
# import com.games.thraxis.framework.lifecycle.TGAppRestarter;
# import com.games.thraxis.framework.listeners.TGListenerRegistry;
# import com.games.thraxis.framework.logging.TGLogger;
# import com.games.thraxis.framework.logging.TGLoggingFactory;
# import com.games.thraxis.framework.rules.TGLoggingRuleEngine;
# import com.games.thraxis.framework.rules.TGRuleEngine;
#
# /##
#  # Created by Zack on 9/26/2017.
#  #/
#
# public abstract class TGBaseRegistry implements TGRegistry {
#
# 	private final TGAppRestarter appRestarter;
# 	private final Context applicationContext;
# 	private final TGEventDistributor<Object> eventDistributor;
# 	private final TGEventTracker<String> eventTracker = new TGSynchronizedEventTracker<>();
# 	private final TGGame game = new TGGame();
# 	private final Map<String, Class<?>> handlersByAction;
# 	private final TGLogger logger = new TGLoggingFactory().create();
# 	private final TGRuleEngine ruleEngine;
# 	private final TGWatchDog watchdog = new TGBaseWatchDog();
#
# 	public TGBaseRegistry(Context context) {
# 		this.applicationContext = context;
# 		this.ruleEngine = new TGLoggingRuleEngine(logger);
# 		this.appRestarter = createAppRestarter();
# 		this.eventDistributor = new TGEventDistributor<>(watchdog, logger);
# 		this.handlersByAction = new TGActivityHandlerMapFactory().create();
# 	}
#
# 	protected abstract TGAppRestarter createAppRestarter();
#
# 	@Override
# 	public TGAppRestarter getAppRestarter() {
# 		return appRestarter;
# 	}
#
# 	@Override
# 	public Context getApplicationContext() {
# 		return applicationContext;
# 	}
#
# 	public TGEventDistributor<Object> getEventDistributor() {
# 		return eventDistributor;
# 	}
#
# 	public TGPublisher<String, Object> getEventPublisher() {
# 		return eventDistributor;
# 	}
#
# 	@Override
# 	public TGEventTracker<String> getEventTracker() {
# 		return eventTracker;
# 	}
#
# 	public TGGame getGame() {
# 		return game;
# 	}
#
# 	public TGListenerRegistry<Object> getListenerRegistry() {
# 		return eventDistributor;
# 	}
#
# 	@Override
# 	public TGLogger getLogger() {
# 		return logger;
# 	}
#
# 	@Override
# 	public TGRuleEngine getRuleEngine() {
# 		return null;
# 	}
#
# 	public TGWatchDog getWatchdog() {
# 		return watchdog;
# 	}
# }
import logging
from abc import ABC

from application.handler_map_factory import TGHandlerMapFactory
from eventhandling.event_distributor import TGEventDistributor
from factories.logging_rule_engine_factory import TGLoggingRuleEngineFactory


class TGAbstractRegistry(ABC):
    def __init__(self):
        self.rule_engine = TGLoggingRuleEngineFactory().create()
        self.logger = logging.getLogger()
        self.event_distributor = TGEventDistributor(logging.getLogger())
        self.handler_map_factory = TGHandlerMapFactory().create()

    # 		this.applicationContext = context;
    # 		this.ruleEngine = new TGLoggingRuleEngine(logger);
    # 		this.appRestarter = createAppRestarter();
    # 		this.eventDistributor = new TGEventDistributor<>(watchdog, logger);
    # 		this.handlersByAction = new TGActivityHandlerMapFactory().create();
