# Logging problem 02 - Experiment with data categories

## Problem statement
Experiment with the different data categories available to the compliant logger.

## Motivation
The goal of this problem is to get you familiar with different data categories provided in `compliant_logging`.

## Out of scope
_stack trace prefixing_ is out of scope for this problem and will be covered in [problem 03](./logging-03.md).

## Prerequisites
You should be familiar with how to set up a "compliant logger" as illustrated in [problem 01](./logging-01.md).

## Guidance
The component we will be working on in this problem is [log_data_category](../../shrike-examples/components/log_data_category).

### Prepare your component script
Open [log_data_category_script.py](../../shrike-examples/contoso/log_data_category_script.py) file. Here you'll need to import relevant libraries, set up logger, and log your messages.

#### Import relevant libraries
First you need to import the required libraries same as [problem 01](./logging-01.md). In addition, you need the `DataCategory` class from `shrike.compliant_logging.constants`.

#### Implement the `main()` method
As usual, you need to set up a "compliant logger" named `logger` as shown in [problem 01](./logging-01.md).
The `DataCategory` Enum class has two values: `PRIVATE` and `PUBLIC`. By default, `compliant_logging` will use `PRIVATE`, where you will not be able to view the log in an eyes-off environment. To see the difference in eyes-on, log one message with each different `DataCategory`:
```python
logger.info("<your-message", category=<your-datacategory>)
```
Also, to see the default category, add
```python
logger.info("<your-message")
```
Note that to easily differentiate in logs, please use a different message each time.

### Submit your experiment

To submit your experiment with the parameter value defined in the config file, just run the command shown at the top of the experiment python file [demo_log_data_category.py](../../shrike-examples/pipelines/experiments/demo_log_data_category.py).

### Check the logs
Once your experiment has executed successfully, click on the component, then on "Outputs + logs". In the driver log (usually called "70_driver_log.txt"), you should see your `PUBLIC` log lines prefixed with `SystemLog:`, and other log lines (`PRIVATE` or undefined category) without any prefix (i.e., something like `INFO:contoso.log_data_category_script:<my-message>`)

### Links to successful execution
A successful run of the experiment can be found [here](https://ml.azure.com/experiments/id/713d1c98-a82a-4aa0-a772-1ab833da3bb4/runs/1fa381f1-2af0-4a05-b1be-f7fd9749a492?wsid=/subscriptions/48bbc269-ce89-4f6f-9a12-c6f91fcb772d/resourcegroups/aml1p-rg/workspaces/aml1p-ml-wus2&tid=72f988bf-86f1-41af-91ab-2d7cd011db47). (This is mostly for internal use, as you likely will not have access to that workspace.)