import logging
import gunicorn.glogging


class HealthzFilter(logging.Filter):
    def filter(self, record):
        return "/healthz" not in record.getMessage()


class Logger(gunicorn.glogging.Logger):
    def setup(self, cfg):
        super().setup(cfg)
        logger = logging.getLogger("gunicorn.access")
        logger.addFilter(HealthzFilter())
