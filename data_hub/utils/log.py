# import structlog


# class Logging:
#     def __init__(self) -> None:
#         structlog.configure(
#             processors=[
#                 structlog.stdlib.filter_by_level,
#                 structlog.stdlib.add_logger_name,
#                 structlog.stdlib.add_log_level,
#                 structlog.stdlib.PositionalArgumentsFormatter(),
#                 structlog.processors.TimeStamper(fmt="iso"),
#                 structlog.processors.StackInfoRenderer(),
#                 structlog.processors.format_exc_info,
#                 structlog.processors.JSONRenderer(),
#             ],
#             context_class=dict,
#             logger_factory=structlog.stdlib.LoggerFactory(),
#             wrapper_class=structlog.stdlib.BoundLogger,
#             cache_logger_on_first_use=True,
#         )
#         self.logger = structlog.get_logger()

#     def get_logger(self):
#         return self.logger


# log = Logging()
# logger = log.get_logger()

import logging
import datetime
import json


class CustomJSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "module": record.module,
            "message": record.msg,
        }
        return json.dumps(log_data)


def create_custom_logger(logger_name, log_level=logging.INFO):
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    formatter = CustomJSONFormatter()

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


logger = create_custom_logger("data_hub_logger", log_level=logging.INFO)
