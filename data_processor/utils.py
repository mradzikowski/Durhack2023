import logging
from functools import lru_cache

from rich.console import Console
from rich.logging import RichHandler

console = Console(color_system="256", width=200, style="blue")


@lru_cache
def get_logger(module_name):
    """
    Helper logger that has rich console with highlighting options
    :param module_name: module name
    :return:
    """
    logger = logging.getLogger(module_name)
    handler = RichHandler(
        rich_tracebacks=True,
        console=console,
        tracebacks_show_locals=True,
    )
    handler.setFormatter(
        logging.Formatter(
            f"{module_name} [ %(threadName)s:%(funcName)s:%(lineno)d ] - %(message)s",
        ),
    )
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger
