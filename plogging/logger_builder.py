from pathlib import Path
from typing import Any, Optional, Tuple, List, Callable, Dict
import logging
from dataclasses import dataclass

from .constants.formats import LOGGING_FORMATTER, _level_types, _handler_types
from .exceptions import LoggerConfigurationError


def create_file_handler(level: int, file_path: Path) -> logging.Handler:
    try:
        fh = logging.FileHandler(file_path)
    except FileNotFoundError:
        Path(file_path).parent.mkdir(parents=True)
        fh = logging.FileHandler(file_path)
    fh.setLevel(level=level)
    fh.setFormatter(LOGGING_FORMATTER)
    return fh


def create_stream_handler(level: int, file_path: Optional[Path]) -> logging.Handler:
    sh = logging.StreamHandler()
    sh.setLevel(level=level)
    sh.setFormatter(LOGGING_FORMATTER)
    return sh


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

    def __init__(
        self,
        name: str,
        level: List[_level_types] = [logging.INFO],
        handler_types: List[_handler_types] = ["stream"],
        file_path: Optional[Path] = None,
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
        self.handlers = [
            self._handler_types_map[ht](ll, file_path)
            for ht, ll in zip(handler_types, _levels)
        ]

    def __call__(self) -> Any:
        return self._build_logger()

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
