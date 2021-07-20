"""
AzureML Run wrapper for integration
"""
import logging
import json
import os
import traceback

from .log_utils import log, DataCategory

########################
#### AML RUN OBJECT ####
########################


class AmlRunWrapper:
    """The purpose of this wrapper is to allow to import azureml.core.run
    only when "attached" from the module main function
    because we need to turn it off in detonation chamber
    """

    _recipe_azureml_run = None
    _metrics_file_path = None

    # https://python-patterns.guide/gang-of-four/singleton/
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AmlRunWrapper, cls).__new__(cls)
            # Put any initialization here.
        return cls._instance

    def setup(self, **kwargs):
        """Sets up based on keyword arguments

        Args:
            **kwargs (dict): keyword arguments

        Notes (Keyword Args):
            run (azureml.core.run.Run): if provided, use this run object to report metrics/logs
            attach (bool): attach to the current Run.get_context()
            output_file (str): path to a file for writing metric records in json
        """
        if kwargs.get("attach", False):
            log(
                logging.DEBUG,
                DataCategory.ONLY_PUBLIC_DATA,
                "Creating instance of azureml.core.run.Run",
            )
            # IMPORTANT: keep this import outside of top level
            # because this requires aml connection
            try:
                from azureml.core.run import Run

                self._recipe_azureml_run = Run.get_context(allow_offline=True)
            except:
                # if running in detonation chamber, this will fail due to lack of connectivity
                log(
                    logging.CRITICAL,
                    DataCategory.ONLY_PUBLIC_DATA,
                    "Obtaining Run.get_context() resulted in an exception: {}".format(
                        traceback.format_exc()
                    ),
                )
                self._recipe_azureml_run = None

        elif "run" in kwargs:
            self._recipe_azureml_run = kwargs.get("run")

        if "output_file" in kwargs:
            self._metrics_file_path = kwargs.get("output_file")
            log(
                logging.INFO,
                DataCategory.ONLY_PUBLIC_DATA,
                "Will write metrics in {}".format(self._metrics_file_path),
            )

    def __getattr__(self, name):
        """This is a hack of the Run class to allow to call any of its methods.
        Whatever method from Run you'll call, it will forward to it after
        making sure of the DataCategory.
        """

        def _transient_method(*args, **kwargs):
            log(
                logging.DEBUG,
                DataCategory.CONTAINS_PRIVATE_DATA,
                "Run.{}() called while offline, with args={} and kwargs={}".format(
                    name, args, kwargs
                ),
            )
            if self._metrics_file_path:
                with open(self._metrics_file_path, "a") as ofile:
                    ofile.write(
                        json.dumps(
                            {
                                "log_method": name,
                                "log_args": list(args),
                                "log_kwargs": kwargs,
                            }
                        )
                    )
                    ofile.write("\n")
            if self._recipe_azureml_run:
                func = getattr(self._recipe_azureml_run, name)
                # try to actually run the function
                try:
                    func(*args, **kwargs)
                except BaseException as run_exception:
                    log(
                        logging.WARNING,
                        DataCategory.ONLY_PUBLIC_DATA,
                        "Trying to run AML Run.{} led to an exception type {}.".format(
                            name, run_exception.__class__.__name__
                        ),
                    )

        return _transient_method


def aml_run_attach():
    """Attach AML run object"""
    AmlRunWrapper().setup(attach=True)


###########################
### AML METRICS LOGGING ###
###########################


def log_directory(data_category, key, path, verbose=False):
    """Counts files, dirs, size in a given directory and record
    as AML metric (or StdOut)

    Args:
        data_category (DataCategory) : public or private?
        key (string) : metric identifier in step run
        path (string) : path to directory to scan
        verbose (bool) : list all files in directory as metrics
    """
    run = AmlRunWrapper()
    run.setup(attach=True)

    count_files = 0
    count_dirs = 0
    total_size = 0
    for base_dir, subdirs, files in os.walk(path):
        count_dirs += len(subdirs)
        count_files += len(files)
        for entry in files:
            entry_size = os.path.getsize(os.path.join(base_dir, entry))
            total_size += entry_size
            if verbose:
                log(
                    logging.INFO,
                    data_category,
                    "Scan {} -- found file: {} -- size {}".format(
                        key, os.path.join(base_dir, entry), entry_size
                    ),
                )

    run.log_row(key, dirs=count_dirs, files=count_files, size=total_size)

    log(
        logging.INFO,
        data_category,
        "Scan {} -- path {} -- found {} files, {} dirs, total size {}".format(
            key, path, count_files, count_dirs, total_size
        ),
    )
    run.flush()


def log_metric(data_category, key, value):
    """log metric in AML UI """
    # always, just print in logs
    log(logging.INFO, data_category, "AML Metric({}={})".format(key, value))
    if data_category == DataCategory.ONLY_PUBLIC_DATA:
        # if public, ask azureml to record (if azureml attached)
        run = AmlRunWrapper()
        run.setup(attach=True)
        run.log(key, value)
        run.flush()


def log_row(data_category, key, **kwargs):
    """log row in AML workspace UI"""
    # always, just print in logs
    log(logging.INFO, data_category, "AML MetricRow({}, {})".format(key, kwargs))
    if data_category == DataCategory.ONLY_PUBLIC_DATA:
        # if public, ask azureml to record (if azureml attached)
        run = AmlRunWrapper()
        run.setup(attach=True)
        run.log_row(key, **kwargs)
        run.flush()


def log_list(data_category, list_name, value, **kwargs):
    """log list in AML workspace UI """
    # always, just print in logs
    log(logging.INFO, data_category, "AML MetricList({}, {})".format(list_name, value))
    if data_category == DataCategory.ONLY_PUBLIC_DATA:
        # if public, ask azureml to record (if azureml attached)
        run = AmlRunWrapper()
        run.setup(attach=True)
        run.log_list(name=list_name, value=value, **kwargs)
        run.flush()


def log_table(data_category, table_name, value, **kwargs):
    """log table in AML workspace UI"""
    # always, just print in logs
    log(
        logging.INFO, data_category, "AML MetricTable({}, {})".format(table_name, value)
    )
    if data_category == DataCategory.ONLY_PUBLIC_DATA:
        # if public, ask azureml to record (if azureml attached)
        run = AmlRunWrapper()
        run.setup(attach=True)
        run.log_table(table_name, value, **kwargs)
        run.flush()


def log_image(data_category, image_name, path=None, plot=None, **kwargs):
    """log image in AML workspace UI"""
    # always, just print in logs
    log(logging.INFO, data_category, "AML MetricImage({})".format(image_name))
    if data_category == DataCategory.ONLY_PUBLIC_DATA:
        # if public, ask azureml to record (if azureml attached)
        run = AmlRunWrapper()
        run.setup(attach=True)
        run.log_image(image_name, path, plot, **kwargs)
        run.flush()
