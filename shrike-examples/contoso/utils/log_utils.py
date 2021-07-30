""" Compliant logging helper utils. """
import logging
import datetime

from shrike.compliant_logging import (
    DataCategory as DataCategoryMLUtils,
    enable_compliant_logging,
)


__all__ = ["DataCategory", "CompliantLoggerInitializer", "log"]


class DataCategory:
    """
    Define data categories for compliant logger.
    """

    CONTAINS_PRIVATE_DATA = DataCategoryMLUtils.PRIVATE
    ONLY_PUBLIC_DATA = DataCategoryMLUtils.PUBLIC


class CompliantLoggerInitializer(object):
    """
    This classes initializes the logging only once.
    As a Singleton, any new call will not re-create the logging handler.
    """

    # singleton pattern from https://python-patterns.guide/gang-of-four/singleton/
    _instance = None

    def __new__(cls, level):
        """
        Enables compliant logging and sets log-level to level if instance does not exist.
        Updates log-level otherwise.
        """
        if cls._instance is None:
            # if this is the first time we're initializing
            print(
                "Initializing Compliant logger once at level {}".format(
                    logging.getLevelName(level)
                )
            )

            cls._instance = super(CompliantLoggerInitializer, cls).__new__(cls)

            enable_compliant_logging()

            logger = logging.getLogger()
            logger.setLevel(level)
            for handler in logger.handlers:
                handler.setLevel(level)
            stdout_handler = logging.StreamHandler()
            stdout_handler.setLevel(level)
            logger.addHandler(stdout_handler)
        else:
            # if this is not the first time, just reset the level
            print(
                "Updating SmartCompose logger to level {}".format(
                    logging.getLevelName(level)
                )
            )
            logger = logging.getLogger()
            logger.setLevel(level)
            for handler in logger.handlers:
                handler.setLevel(level)

        return cls._instance


CompliantLoggerInitializer(logging.INFO)  # initialize at least once


def log(level: int, data_category: DataCategoryMLUtils, message: str):
    """
    Log the message at a given level (from the standard logging package: ERROR, INFO, DEBUG etc).
    Add a datetime prefix to the log message, and a SystemLog: prefix provided it is public data.
    The data_category can be one of CONTAINS_PRIVATE_DATA or ONLY_PUBLIC_DATA.

    Args:
        level: logging level, best set by using logging.(INFO|DEBUG|WARNING) etc
        data_category: whether message contains private or public data
        message: message to log
    """
    message = "{}\t{}\t{}".format(
        datetime.datetime.now(), logging.getLevelName(level), message
    )
    logging.getLogger().log(level=level, msg=message, category=data_category)
