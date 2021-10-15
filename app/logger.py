"""
Logger.
"""
import logging
import os
import sys
from collections import OrderedDict
from datetime import datetime
from logging import LogRecord
from typing import List

from pythonjsonlogger import jsonlogger

from .constants import APP_NAME


class JsonFormatter(jsonlogger.JsonFormatter):
    def parse(self) -> List[str]:
        """parse"""
        return ["timestamp", "requester", "payload", "level", "name", "message"]

    def add_fields(self, log_record: OrderedDict, record: LogRecord, message_dict: dict) -> None:
        """add_fields"""
        super().add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            log_record["timestamp"] = datetime.utcnow().isoformat()
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname


def get_logger() -> logging.Logger:
    logger = logging.getLogger(APP_NAME)
    logger.setLevel(os.getenv("LOG_LEVEL", default="INFO"))

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)

    # Overriding sqlalchemy's parent logger
    logging.getLogger("sqlalchemy.engine").setLevel(level=os.environ.get("SQL_LOG_LEVEL", default="INFO"))

    return logger


logger = get_logger()
