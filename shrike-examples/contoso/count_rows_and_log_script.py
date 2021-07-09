import argparse
import pandas as pd
import logging
import shrike
from shrike.compliant_logging import enable_compliant_logging
import os

def get_arg_parser(parser=None):
    """Parse the command line arguments for merge using argparse

    Args:
        parser (argparse.ArgumentParser or CompliantArgumentParser): an argument parser instance

    Returns:
        ArgumentParser: the argument parser instance

    Notes:
        if parser is None, creates a new parser instance
    """
    # add arguments that are specific to the component
    if parser is None:
        parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("--input_data", required=True, type=str, help="the input data")

    return parser


def main():
    """The main function"""

    # get the arguments
    parser = get_arg_parser()
    args = parser.parse_args()
    args = vars(args)

    # initialze logger
    enable_compliant_logging()
    logger = logging.getLogger(__name__)

    # path of the debug dataset
    logger.info("The input dataset path is: '" + str(args["input_data"]) + "'.")

    # read the dataset
    df = pd.read_csv(args["input_data"] + "/iris.csv")

    # count the number of rows
    num_rows = df.count()[0]

    # print the result
    logger.info("The dataset contains " + str(num_rows) + " rows.")

    # get the average file size
    file_no = 0
    file_size = 0
    for path, dirs, files in os.walk(args["input_data"]):
        for f in files:
            fp = os.path.join(path, f)
            file_size += os.path.getsize(fp)
            file_no += 1
    logger.info(f"There are {file_no} files in total.")
    logger.info(f"Total file size is {file_size} bytes.")
    avg_file_size = file_size / file_no
    logger.info(f"The average file size is {avg_file_size} bytes.")


if __name__ == "__main__":
    main()
