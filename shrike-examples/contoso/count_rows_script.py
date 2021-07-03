import argparse
import pandas as pd

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

    # path of the debug dataset
    print("The input dataset path is: '" + str(args["input_data"]) + "'.")

    # read the dataset
    df = pd.read_csv(args["input_data"] + "/iris.csv")
    
    # count the number of rows
    num_rows = df.count()[0]

    # print the result
    print("The dataset contains " + str(num_rows) + " rows.")

if __name__ == "__main__":
    main()
