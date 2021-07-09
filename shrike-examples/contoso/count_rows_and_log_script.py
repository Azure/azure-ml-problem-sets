import argparse
import pandas as pd
# To-Do: import required libraries


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

    # To-Do: parse arguments as in pipelines-problem-03

    return parser


def main():
    """The main function"""

    # get the arguments
    parser = get_arg_parser()
    args = parser.parse_args()
    args = vars(args)

    # To-Do: log the number of rows and file size


if __name__ == "__main__":
    main()
