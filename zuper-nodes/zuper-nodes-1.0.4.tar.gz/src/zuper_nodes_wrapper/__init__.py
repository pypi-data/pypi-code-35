import logging

from zuper_nodes import logger as aido_nodes_logger

logger = aido_nodes_logger.getChild('wrapper')

logger_interaction = logger.getChild("interaction")

logger_interaction.setLevel(logging.CRITICAL)

from .wrapper import *
