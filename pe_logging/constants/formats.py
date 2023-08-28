from logging import Formatter
from typing import Literal, Union, Tuple

LOG_FORMAT = "[%(name)s ~ %(levelname)s @ %(asctime)s]: \n  %(message)s"
LOG_DATE_FORMAT = "%H:%M:%S %a(%d/%m)"
LOGGING_FORMATTER = Formatter(LOG_FORMAT, LOG_DATE_FORMAT)

_handler_types = Literal["file", "stream"]
_level_types = Union[Tuple[int], int]
