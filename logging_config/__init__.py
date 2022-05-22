import os
import logging

import colorama


# Environment variable to set for development mode.
DEV_MODE = "LOGGING_CONFIG_DEV_MODE"


def set_default():
    colorama.init()
    __setup_root_logger()


# https://stackoverflow.com/a/384125
class ColoredFormatter(logging.Formatter):
    colors = {
        "DEBUG": colorama.Fore.CYAN,
        "INFO": colorama.Fore.GREEN,
        "WARNING": colorama.Fore.LIGHTRED_EX,
        "ERROR": colorama.Fore.RED,
        "CRITICAL": colorama.Fore.RED,
    }

    def __init__(self, is_detailed: bool = False):
        super(ColoredFormatter, self).__init__("{custom_return}", style="{")

        self._is_detailed = is_detailed

    def format(self, record):
        new_rec = logging.makeLogRecord(vars(record))

        custom_return = (
            f"{new_rec.levelname} - {new_rec.filename}:{new_rec.funcName}():{new_rec.lineno} - {new_rec.msg}"
            if self._is_detailed
            else f"{new_rec.levelname} - {new_rec.msg}"
        )

        new_rec.custom_return = (
            self.colors.get(record.levelname, colorama.Style.RESET_ALL) + custom_return + colorama.Style.RESET_ALL
        )

        return super(ColoredFormatter, self).format(new_rec)


def __setup_root_logger():
    root_logger = logging.getLogger()

    # Logging level.
    root_logger.setLevel(logging.INFO)
    if os.getenv(DEV_MODE, None):
        root_logger.setLevel(logging.DEBUG)

    # Handlers, Filters and Formatters.
    detailed_levels = (logging.DEBUG,)

    detailed_handler = logging.StreamHandler()
    detailed_handler.setLevel(logging.DEBUG)
    detailed_handler.addFilter(lambda record: record.levelno in detailed_levels)
    detailed_handler.setFormatter(ColoredFormatter(is_detailed=True))

    basic_handler = logging.StreamHandler()
    basic_handler.setLevel(logging.INFO)
    basic_handler.addFilter(lambda record: record.levelno not in detailed_levels)
    basic_handler.setFormatter(ColoredFormatter(is_detailed=False))

    root_logger.addHandler(detailed_handler)
    root_logger.addHandler(basic_handler)
