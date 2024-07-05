import logging
import logging.config
import sys
from pathlib import Path


BASE_LOGGER_DIR: Path = Path().cwd() / "logs"


class BaseLog:
    """
    Base logging configuration.

    Default settings:

        level = 1 (DEBUG)

        rotation = False

    """

    def __init__(
        self,
        filename: str,
        level: str | int = 1,
        logger_name: str = "",
        base_logger_dir: Path | str = None,
    ):
        self._filename: str = filename
        self._level: str | int = level
        self._logger_name: str = logger_name
        self._base_logger_dir: Path | str = base_logger_dir or BASE_LOGGER_DIR
        self._base_logger_dir.mkdir(exist_ok=True)
        self._format: str = "[%(asctime)s] %(levelname)s [%(filename)s:%(name)s.%(funcName)s:%(lineno)d]: %(message)s"
        self._logger_conf: dict = {
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {"base": {"format": self._format, "datefmt": "%Y-%m-%d %H:%M:%S"}},
            "handlers": {
                "errors": {
                    "class": "logging.FileHandler",
                    "level": "ERROR",
                    "formatter": "base",
                    "filename": f"{self._base_logger_dir}/errors.log",
                    "mode": "a",
                },
            },
            "loggers": {},
        }

    def update_config(self, config: dict = None) -> dict:
        if config:
            self._logger_conf.update(**config)

        return self._logger_conf

    def create_default(
        self,
    ) -> logging.Logger:
        self._logger_conf["handlers"]["console"] = {
            "class": "logging.StreamHandler",
            "level": self._level,
            "formatter": "base",
            "stream": sys.stdout,
        }
        self._logger_conf["loggers"][self._logger_name] = {
            "level": self._level,
            "handlers": ["console", "errors"],
            "filters": [],
            "propagate": 0,
        }
        logging.config.dictConfig(self._logger_conf)
        logger: logging.Logger = logging.getLogger(self._logger_name)

        return logger

    def add_logger(self, logger_name: str, level: str | int) -> logging.Logger:
        if not self._base_logger_dir.exists():
            self._base_logger_dir.mkdir(parents=True)
        logger_name: str = logger_name if logger_name else f"{self.__class__.__name__}"
        self._logger_conf["handlers"][logger_name] = {
            "class": "logging.handlers.RotatingFileHandler",
            "backupCount": 2,
            "encoding": None,
            "delay": 0,
            "level": "NOTSET",
            "formatter": "base",
            "filename": str(self._base_logger_dir / self._filename),
            "mode": "a",
        }
        self._logger_conf["loggers"][logger_name] = {
            "level": level,
            "handlers": ["console", "errors", logger_name],
            "filters": [],
            "propagate": 1,
        }
        if self._logger_conf["loggers"].get("main", {}):
            self._logger_conf["loggers"][logger_name]["handlers"].append("main")

        logging.config.dictConfig(self._logger_conf)
        logger: logging.Logger = logging.getLogger(logger_name)

        return logger


def make_logger(logger_name: str, level: int | str = 1, base_logger_dir: Path | str = "") -> logging.Logger:
    filename = f"{logger_name}.logs"
    base_log = BaseLog(
        filename=filename,
        level=level,
        logger_name=logger_name,
        base_logger_dir=base_logger_dir,
    )
    base_log.update_config()

    return base_log.create_default()
