import logging
import shrike
from shrike.compliant_logging import enable_compliant_logging
from shrike.compliant_logging.constants import DataCategory


def main():
    """The main function"""
    enable_compliant_logging()
    logger = logging.getLogger(__name__)
    logger.info("This is public", category=DataCategory.PUBLIC)
    logger.info("This is private", category=DataCategory.PRIVATE)


if __name__ == "__main__":
    main()
