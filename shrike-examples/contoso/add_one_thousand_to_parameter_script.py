import argparse


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

    parser.add_argument(
        "--value",
        required=False,
        type=int,
        default=100,
        help="the value on which we will operate",
    )
    return parser


def main():
    """The main function"""

    # get the arguments
    parser = get_arg_parser()
    args = parser.parse_args()
    args = vars(args)

    # this shows a basic operation on the value passed as parameter
    value = args["value"]
    operand = 1000
    result = value + operand
    print(
        "The value passed as parameter is: "
        + str(value)
        + ". We computed: "
        + str(value)
        + " + "
        + str(operand)
        + " = "
        + str(result)
        + "."
    )


if __name__ == "__main__":
    main()
