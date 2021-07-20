"""
Utility functions for argument parsing
"""
import argparse


def str2bool(val):
    """
    Resolving boolean arguments if they are not given in the standard format

    Arguments:
        val (bool or string): boolean argument type

    Returns:
        bool: the desired value {True, False}
    """
    if isinstance(val, bool):
        return val
    if isinstance(val, str):
        if val.lower() in ("yes", "true", "t", "y", "1"):
            return True
        elif val.lower() in ("no", "false", "f", "n", "0"):
            return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


def str2intlist(val):
    """Converts comma separated string of integers into list of integers

    Args:
        val (str): comma separate string of integers
    """
    return commastring2list(int)(val)


def commastring2list(output_type=str):
    """Returns a lambda function which converts a comma separated string into a list of a given type

    Args:
        output_type (function, optional): string type conversion function. Defaults to str.

    Returns:
        function: lambda function
    """
    return lambda input_str: list(map(output_type, input_str.split(",")))
