"""
This script is for debugging and probing
"""
import os
import sys
import argparse
import logging
import traceback
import uuid
from subprocess import PIPE
from subprocess import run as subprocess_run
import pkg_resources

from utils import (
    log,
    DataCategory,
    str2bool,
    CompliantLoggerInitializer,
    log_row,
    log_directory,
    aml_run_attach,
)


def get_arg_parser(parser=None):
    """
    Adds module arguments to a given argument parser.

    Args:
        parser (argparse.ArgumentParser or CompliantArgumentParser): an argument parser instance

    Returns:
        CompliantArgumentParser: the argument parser instance

    Notes:
        if parser is None, creates a new parser instance
    """
    if parser is None:
        parser = argparse.ArgumentParser()

    group = parser.add_argument_group("Module I/O")
    group.add_argument(
        "--data_path",
        dest="data_path",
        default=None,
        type=str,
        help="named input from aether",
    )
    group.add_argument(
        "--results",
        dest="results",
        default=None,
        type=str,
        help="intentionally fail, raises an Exception with error message",
    )

    group = parser.add_argument_group("Probing options")
    group.add_argument(
        "--scan_deps",
        dest="scan_deps",
        default=False,
        type=str2bool,
        help="lists existing python modules with their versions",
    )
    group.add_argument(
        "--scan_env",
        dest="scan_env",
        default=False,
        type=str2bool,
        help="lists existing environment variables",
    )
    group.add_argument(
        "--scan_args",
        dest="scan_args",
        default=False,
        type=str2bool,
        help="lists existing arguments to this script",
    )
    group.add_argument(
        "--scan_nvidia",
        dest="scan_nvidia",
        default=False,
        type=str2bool,
        help="uses nvidia-smi to scan drivers etc",
    )
    group.add_argument(
        "--scan_input",
        dest="scan_input",
        default=False,
        type=str2bool,
        help="count files and dirs in provided --data_path",
    )
    group.add_argument(
        "--scan_output",
        dest="scan_output",
        default=False,
        type=str2bool,
        help="count files and dirs in --results after execution",
    )
    group.add_argument(
        "--prefix",
        default="SystemLog:",
        type=str,
        help="prefix for prints/logs for testing (default 'SystemLog:')",
    )
    group.add_argument(
        "--fail",
        dest="fail",
        default=False,
        type=str2bool,
        help="intentionally fail, raises an Exception with error message",
    )
    group.add_argument(
        "--windows_compute",
        dest="windows_compute",
        type=str2bool,
        required=False,
        default=False,
        help="test compute target in windows os",
    )

    group = parser.add_argument_group("AML run arguments [generic]")
    group.add_argument(
        "--verbose", "-v", default=False, type=str2bool, help="prints debug"
    )
    group.add_argument(
        "--log_in_aml",
        dest="log_in_aml",
        type=str2bool,
        required=False,
        default=False,
        help="send metrics to AzureML",
    )

    return parser


def run(args):
    """Probe with arguments

    Args:
        args (argparse.namespace): command line arguments provided to script
    """
    # print with or without prefix just to check if module is working
    print("Hello World! (probe, print)")  # this won't show up in stdout
    print(args.prefix + "Hello World! (probe, print, prefix)")  # this will

    # create console handler and set level to info
    logger = logging.getLogger(__name__)

    # if provided --results, use to store log file output.log
    if args.results:
        output_file_path = os.path.join(
            args.results, "{}.log".format(str(uuid.uuid4()))
        )
        log(
            logging.INFO,
            DataCategory.ONLY_PUBLIC_DATA,
            "Printing logs in result file: {}".format(output_file_path),
        )
        os.makedirs(args.results, exist_ok=True)
        result_handler = logging.FileHandler(output_file_path)
        # result_handler.setFormatter(systemlog_formatter)
        logger.addHandler(result_handler)

    # trying a couple of logs
    logger.debug("Hello World! (probe, log, debug)")
    logger.info("Hello World! (probe, log, info)")
    logger.warning("Hello World! (probe, log, warning)")
    logger.critical("Hello World! (probe, log, critical)")

    # lists arguments
    if args.scan_args:
        log(
            logging.INFO,
            DataCategory.ONLY_PUBLIC_DATA,
            "Probe arguments: {}".format(" ".join(sys.argv)),
        )

    # Windows compute test: run a hello-world windows command
    # It could be replaced by a call to .exe file
    if args.windows_compute:
        try:
            windows_command = ["windows_run.cmd"]
            windows_result = subprocess_run(
                windows_command,
                stdout=PIPE,
                stderr=PIPE,
                universal_newlines=False,
                check=False,
            )
            windows_result_str = (
                str(windows_result.returncode)
                + ":"
                + str(windows_result.stdout)
                + ":"
                + str(windows_result.stderr)
            )
            log(
                logging.INFO,
                DataCategory.ONLY_PUBLIC_DATA,
                "windows-command> {}".format(windows_result_str),
            )
        except:
            log(
                logging.INFO,
                DataCategory.ONLY_PUBLIC_DATA,
                "Running windows-command has raised an exception: {}".format(
                    traceback.format_exc()
                ),
            )

    # lists all the available python modules via pip
    if args.scan_deps:
        log(
            logging.INFO,
            DataCategory.ONLY_PUBLIC_DATA,
            "Probe has python version {}".format(str(sys.version_info)),
        )
        log_row(
            DataCategory.ONLY_PUBLIC_DATA,
            "python_version",
            version=str(sys.version_info),
        )

        for i in pkg_resources.working_set.__iter__():
            log(
                logging.INFO,
                DataCategory.ONLY_PUBLIC_DATA,
                "Probe has python package {} installed with version {}".format(
                    i.key, i.version
                ),
            )
            log_row(
                DataCategory.ONLY_PUBLIC_DATA,
                "python_package",
                package=i.key,
                version=i.version,
            )

    # lists all the available environment variables
    if args.scan_env:
        for k in os.environ:
            log(
                logging.INFO,
                DataCategory.ONLY_PUBLIC_DATA,
                f"Probe env variable {k} exists",
            )

    if args.scan_input:
        log(
            logging.INFO,
            DataCategory.ONLY_PUBLIC_DATA,
            "Probe begin scanning --data_path {}".format(args.data_path),
        )
        if args.data_path is None:
            logger.critical(
                "Probe needs a --data_path argument to execute --scan-input"
            )
        else:
            log_directory(DataCategory.ONLY_PUBLIC_DATA, "scan_input", args.data_path)

    # nvidia test
    if args.scan_nvidia:
        try:
            command = ["nvidia-smi"]
            nvidia_result = subprocess_run(
                command, stdout=PIPE, stderr=PIPE, universal_newlines=False, check=False
            )
            nvidia_result_str = (
                str(nvidia_result.returncode)
                + ":"
                + str(nvidia_result.stdout)
                + ":"
                + str(nvidia_result.stderr)
            )
            log(
                logging.INFO,
                DataCategory.ONLY_PUBLIC_DATA,
                "nvidia-smi> {}".format(nvidia_result_str),
            )
        except FileNotFoundError:
            log(
                logging.INFO,
                DataCategory.ONLY_PUBLIC_DATA,
                "Running nvidia-smi has raised an exception: {}".format(
                    traceback.format_exc()
                ),
            )

    # testing exceptions logging
    if args.fail:
        raise Exception(args.prefix + "The probe failed intentionally.")

    if args.scan_output:
        log(
            logging.INFO,
            DataCategory.ONLY_PUBLIC_DATA,
            "Probe begin scanning --results {}".format(args.results),
        )
        if args.results is None:
            logger.critical("Probe needs a --results argument to execute --scan-output")
        else:
            log_directory(DataCategory.ONLY_PUBLIC_DATA, "scan_output", args.results)


def main(flags=None):
    """AML module main, parses arguments and executes run() function from smartcompose code

    Args:
        flags (List[str]): list of flags to feed script, useful for debugging. Defaults to None.
    """
    parser = get_arg_parser()

    # if argument parsing fails, will print the exception in SystemLog and exit
    # if any unknown argument, will print WARNING in SystemLog
    args, _ = parser.parse_known_args(flags)

    # setup internal aml logger
    if args.verbose:
        CompliantLoggerInitializer(logging.DEBUG)
    else:
        CompliantLoggerInitializer(logging.INFO)

    if args.log_in_aml:
        # imports azureml.core.run and get run from context
        aml_run_attach()

    log(
        logging.INFO,
        DataCategory.ONLY_PUBLIC_DATA,
        "Running module with arguments: {}".format(args),
    )
    run(args)


if __name__ == "__main__":
    main()
