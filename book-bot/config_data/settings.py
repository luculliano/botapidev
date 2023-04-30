import logging.config
import sys


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default_formatter": {
            "format": "%(asctime)s [%(levelname)s] %(filename)s: %(message)s"
        },
    },
    # specify handlers
    "handlers": {
        "stream_handler": {
            "class": "logging.StreamHandler",
            "formatter": "default_formatter",
            "stream": sys.stdout,
        },
    },
    # specify loggers
    "loggers": {
        "stream": {
            "handlers": ["stream_handler"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("stream")

if __name__ == "__main__":
    logger.info("check the output")
