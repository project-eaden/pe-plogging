from pathlib import Path
from typing import Optional, Tuple, List, Callable, Dict
import logging
from dataclasses import dataclass
from logging import Formatter

from .constants.formats import (
    LOG_FORMAT,
    ONE_LINE_LOG_FORMAT,
    _level_types,
    _handler_types,
)
from .exceptions import LoggerConfigurationError


def create_file_handler(
    level: int, file_path: Path, multiline: bool = True
) -> logging.Handler:
    try:
        fh = logging.FileHandler(file_path)
    except FileNotFoundError:
        Path(file_path).parent.mkdir(parents=True)
        fh = logging.FileHandler(file_path)
    fh.setLevel(level=level)
    fh.setFormatter(PloggerFormatter() if multiline else PloggerFormatterSingleLine())
    return fh


def create_stream_handler(
    level: int, file_path: Optional[Path], multiline: bool = True
) -> logging.Handler:
    sh = logging.StreamHandler()
    sh.setLevel(level=level)
    sh.setFormatter(PloggerFormatter() if multiline else PloggerFormatterSingleLine())
    return sh


class PloggerFormatter(Formatter):
    light_blue = "\033[0;34m"
    light_green = "\033[0;32m"
    warning = "\033[93m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    lgfmt = LOG_FORMAT

    FORMATS = {
        logging.DEBUG: light_blue + lgfmt + reset,
        logging.INFO: light_green + lgfmt + reset,
        logging.WARNING: yellow + lgfmt + reset,
        logging.ERROR: red + lgfmt + reset,
        logging.CRITICAL: bold_red + lgfmt + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class PloggerFormatterSingleLine(PloggerFormatter):
    lgfmt = ONE_LINE_LOG_FORMAT


class Plogger:
    """
    The factory class for the Project Eaden standard logger for specified handlers.

    Args:
        - `name`[req]: The desired name for the logger
        - `level`[optional]: A **list** of the logging level(s) to use for the
        returned logger instance. If you'd like to specify a logging level
        per handler, then ensure that the order is the same as that of the list
        `handler_type`. If only one level is specified, then it will be applied
        to all the handlers of the resulting logger. The default level applied
        to all handlers is `logging.INFO`
        - `handler_type`[optional]: The **list** of desired handlers for the
        resulting logger instance. Currently supported types are `stream` and
        `file`. The default is a stream handler.
        - `file_path`[optional]: The path containing the logging file to write
        logs from the filehandler to. Required only when a filehandler is
        requested. Recommend a file ending in the extension .log
    """

    _handler_types_map: Dict[str, Callable] = {
        "file": create_file_handler,
        "stream": create_stream_handler,
    }
    _potential_logging_levels: List[str] = [
        "debug",
        "info",
        "warn",
        "warning",
        "error",
        "critical",
    ]

    def __init__(
        self,
        name: str,
        level: List[_level_types] = [logging.INFO],
        handler_types: List[_handler_types] = ["stream"],
        file_path: Optional[Path] = None,
        multiline: bool = True,
    ) -> None:
        self.name = name
        try:
            self.config = LoggingConfig(
                tuple(level),
                tuple(handler_types),
                file_path,
                tuple(self._handler_types_map.keys()),
            )
        except AssertionError as e:
            raise LoggerConfigurationError(e.args[0].format(**{"name": self.name}))

        _levels = level * len(handler_types) if len(level) == 1 else level
        self.handlers: List[logging.Handler] = [
            self._handler_types_map[ht](ll, file_path, multiline)
            for ht, ll in zip(handler_types, _levels)
        ]
        self.logger: logging.Logger = self._build_logger()
        for logging_method in self._potential_logging_levels:
            self.__setattr__(
                logging_method, self.logger.__getattribute__(logging_method)
            )

    def _build_logger(self) -> logging.Logger:
        logger = logging.getLogger(self.name)
        # Set default to minimum, since this is filtered by handlers individually
        logger.setLevel(logging.DEBUG)
        for handler in self.handlers:
            logger.addHandler(handler)
        return logger


@dataclass
class LoggingConfig:
    """A class for checking validity of a given logger configuration"""

    level: Tuple[_level_types, ...] = tuple([logging.INFO])
    handler_types: Tuple[_handler_types, ...] = tuple(["stream"])
    file_path: Optional[Path] = None
    accepted_types: Optional[Tuple[str, ...]] = None

    def __post_init__(self) -> None:
        if "file" in self.handler_types:
            assert self.file_path, "No filepath specified for {name} FileHandler!"

        if (nl := len(self.level)) > 1 and (nh := len(self.handler_types)) > 1:
            assert nl == nh, (
                "If multiple levels are supplied, the number of "
                "specified handlers and specified levels must match! "
                f"You supplied {nl} levels with {nh} handlers."
            )
        assert (
            self.accepted_types
        ), "Misconfiguration error! End user should not see this!"
        for h in self.handler_types:
            assert (
                h in self.accepted_types
            ), f"Invalid handler type, {h}, passed! Valid options are"
            "'stream' and 'file'."
