# Logging problem 01 - Log dataset properties

## Problem statement
Submit a pipeline using the compliant logger to log various properties of the dataset consumed by a component (such as number of records or average of a numerical field, for instance).

## Motivation
The goal of this problem is to get you familiar with how to safely log nonsensitive messages using `shrike.compliant_logging`. This is a very helpful functionality, especially in eyes-off environments.

## Out of scope
_DataCategory_ and _stack trace prefixing_ are out of scope for this problem and will be covered in future problems.

## Prerequisites
This tutorial is based on the solution of [pipelines problem 03](./pipelines-03.md). Please work on it first, and copy your solution over to [components/count_rows_and_log](../../shrike-examples/components/count_rows_and_log) and [contoso/count_rows_and_log_script.py](../../shrike-examples/contoso/count_rows_and_log_script.py).

## Guidance
The component we will be working on in this problem is [count_rows_and_log](../../shrike-examples/components/count_rows_and_log).

### Add required libraries
In this problem, we will rely on `shrike.compliant_logging` to handle the logs. First, you need to add this dependency of `shrike` to your [component_env.yaml](../../shrike-examples/components/count_rows_and_log/component_env.yaml)

### Prepare your component script
Open [count_rows_and_log_script.py](../../shrike-examples/contoso/count_rows_and_log_script.py) file. Here you'll need to import relevant libraries, set up logger, and log your messages.

#### Import relevant libraries
First you need to import 
- the Python built-in library `logging`, 
- and the function `enable_compliant_logging` in `shrike.compliant_logging`

#### Implement the `main()` method
Then, modify your implementation in the `main()` method to use `compliant_logging` instead of the vanilla print function in Python. 

First, set up data-category-aware logging by calling
```python
enable_compliant_logging()
```
Next, initialize the logger class,
```python
logger = logging.getLogger(__name__)
```
Then, locate your code for printing and refactor using `compliant_logging`:
```python
logger.info("<your-original-print-statement>")
```

#### Log more properties
Following the instructions in the previous section, you should be able to log more properties. Now, please try calculating the average file size of the input dataset and logging it.

### Submit your experiment

To submit your experiment with the parameter value defined in the config file, just run the command shown at the top of the experiment python file [demo_count_rows_and_log.py](../../shrike-examples/pipelines/experiments/demo_count_rows_and_log.py).

### Check the logs
Once your experiment has executed successfully, click on the component, then on "Outputs + logs". In the driver log (usually called "70_driver_log.txt"), you should see your log lines prefixed with `INFO:contoso.count_rows_and_log_script:`. Tadaa!

### Links to successful execution
A successful run of the experiment can be found [here](https://ml.azure.com/runs/6ec5b7d1-f09d-478b-886a-d539c95435bb?wsid=/subscriptions/48bbc269-ce89-4f6f-9a12-c6f91fcb772d/resourcegroups/aml1p-rg/workspaces/aml1p-ml-wus2&tid=72f988bf-86f1-41af-91ab-2d7cd011db47). (This is mostly for internal use, as you likely will not have access to that workspace.)
.