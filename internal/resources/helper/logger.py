import logging
import json
from datetime import datetime


class LoggerManager:
    def __init__(self, name):
        self.logger = self._setup_logger(name)

    def _setup_logger(self, name):
        logger = logging.getLogger(name)
        handler = logging.StreamHandler()
        handler.setFormatter(self.JSONFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger

    class JSONFormatter(logging.Formatter):
        def format(self, record):
            log_record = {
                "timestamp": datetime.utcnow().isoformat(),
                "level": record.levelname,
                "message": record.msg,
                "trace_id": record.__dict__.get("trace_id", "")
            }
            return json.dumps(log_record)

    def log(self, level, msg, context=None, **kwargs):
        extra = {
            "trace_id": context.trace_id if context else ""
        }
        self.logger.log(level, msg, extra=extra)

    def info(self, msg, context=None, **kwargs):
        self.log(logging.INFO, msg, context, **kwargs)

    def warn(self, msg, context=None, **kwargs):
        self.log(logging.WARNING, msg, context, **kwargs)

    def error(self, msg, context=None, **kwargs):
        self.log(logging.ERROR, msg, context, **kwargs)
