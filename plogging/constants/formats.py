from typing import Literal, Union, Tuple

LOG_FORMAT = "[%(name)s ~ %(levelname)s @ %(asctime)s]:\x1b[0m \n  %(message)s"
ONE_LINE_LOG_FORMAT = "[%(name)s ~ %(levelname)s @ %(asctime)s]:\x1b[0m%(message)s"
LOG_DATE_FORMAT = "%H:%M:%S %a(%d/%m)"

_handler_types = Literal["file", "stream"]
_level_types = Union[Tuple[int], int]
