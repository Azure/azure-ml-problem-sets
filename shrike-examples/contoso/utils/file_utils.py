"""Class that has various file util scripts"""
import os
import logging

from .log_utils import log, DataCategory


def select_first_file(path):
    """Selects first file in folder, use under assumption there is only one file in folder

    Args:
        path (str): path to directory or file to choose

    Raises:
        ValueError: error raised when there are multiple files in the directory

    Returns:
        str: full path of selected file
    """
    if os.path.isfile(path):
        log(
            logging.INFO,
            DataCategory.ONLY_PUBLIC_DATA,
            "Input is file, selecting {}".format(path),
        )
        return path

    files = os.listdir(path)
    log(
        logging.INFO,
        DataCategory.ONLY_PUBLIC_DATA,
        "Found {} in {}".format(files, path),
    )
    if len(files) != 1:
        raise ValueError("expected exactly one file in directory")
    log(logging.INFO, DataCategory.ONLY_PUBLIC_DATA, "Selecting {}".format(files[0]))
    return os.path.join(path, files[0])
