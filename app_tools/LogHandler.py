from enum import IntEnum
import logging
from logging.handlers import RotatingFileHandler
from pydantic import BaseModel, PrivateAttr
from typing import Optional, Any
from .Singleton import Singleton
from pathlib import Path


class LogLevel(IntEnum):
    INFO = logging.INFO
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR


class LogStorageHandler(BaseModel, metaclass=Singleton):
    logfile: Path
    maxBytes: int
    backupCount: Optional[int] = 1

    _logger: Optional[logging.Logger] = PrivateAttr(default=None)
    _handler: Optional[RotatingFileHandler] = PrivateAttr(default=None)

    def model_post_init(self, __context: Any):
        self.configure_logger()
        self.configure_handler()
        if self._handler not in self._logger.handlers:
            self._logger.addHandler(self._handler)

    def configure_logger(self):
        if self._logger is None:
            self._logger = logging.getLogger('mainLogs')
            self._logger.setLevel(logging.INFO)
            self._logger.info('Logger config completed!')
            # self._logger.propagate = False

    def configure_handler(self):
        if self._handler is None:
            self._handler = RotatingFileHandler(filename=self.logfile, maxBytes=self.maxBytes,
                                                backupCount=self.backupCount, encoding='utf-8')
            self._handler.setLevel(logging.INFO)
            self._logger.info('Handler config completed!')
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            self._handler.setFormatter(formatter)

    def setLevel(self, level: LogLevel) -> None:
        """
        Set logging level for both logger and handler
        (mirrors logging.Logger.setLevel)
        """
        if self._logger:
            self._logger.setLevel(int(level))
        if self._handler:
            self._handler.setLevel(int(level))

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        if self._logger:
            self._logger.info(msg, *args, **kwargs)

    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        if self._logger:
            self._logger.error(msg, *args, **kwargs)

    def critical(self, msg: str, *args: Any, **kwargs: Any) -> None:
        if self._logger:
            self._logger.critical(msg, *args, **kwargs)