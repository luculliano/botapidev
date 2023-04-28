import logging.config
from pathlib import Path
import sys


LOGGING_CONFIG = {
    "version": 1,  # for compataability if ithis config will change in future only
    "disable_existing_loggers": False,  # not disable existing loggers
    "formatters": {
        "default_formatter": {
            "format": "%(asctime)s [%(levelname)s] %(filename)s: %(message)s"
        },
    },
    # specify handlers
    "handlers": {
        # "file_handler": {
        #     "class": "logging.FileHandler",
        #     "formatter": "default_formatter",
        #     "filename": Path(__file__).parent.joinpath("log.log"),
        # },
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
