import logging
import logging.config


def init_logger(log_level: str):
    log_config = {
        "version": 1,
        "loggers": {
            "uvicorn": {
                "level": log_level,
                "propagate": False,
                "handlers": ["uvicorn_handler"],
            }
        },
        "handlers": {
            "uvicorn_handler": {
                "class": "logging.StreamHandler",
                "formatter": "uvicorn_formatter",
                "level": log_level,
            }
        },
        "formatters": {
            "uvicorn_formatter": {
                "format": "%(asctime)s - %(levelname)s - %(message)s",
            },
        },
    }
    logging.config.dictConfig(log_config)


def get_logger() -> logging.Logger:
    return logging.getLogger("uvicorn")
