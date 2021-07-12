# Logging problem 03 - Experiment with stack trace prefixing

## Problem statement
Experiment with the various options about stack trace prefixing (customize the prefix and the exception message, scrub the exception message unless it is in an allowed list).

## Motivation
The goal of this problem is to get you familiar with stack trace prefixing provided in `compliant_logging`.


## Prerequisites
You should have a basic understanding of [exceptions](https://docs.python.org/3.7/library/exceptions.html) in Python. Here we will experiment with the [ZeroDivisionError](https://docs.python.org/3.7/library/exceptions.html#ZeroDivisionError)

## Guidance
The component we will be working on in this problem is [log_stack_trace_prefixing](../../shrike-examples/components/log_stack_trace_prefixing).

### Prepare your component script
Open [log_stack_trace_prefixing_script.py](../../shrike-examples/contoso/log_stack_trace_prefixing_script.py) file. Here you'll need to import relevant libraries, set up logger, and log your messages.

#### Import relevant libraries
First you need to import the required libraries. You will need `prefix_stack_trace` function from `shrike.compliant_logging.exceptions`.

#### Implement `custom_prefix()`
To use the `prefix_stack_trace` decorator and enable a custom prefix, you should use `prefix` argument. Now try decorating the function `custom_prefix()`:
```python
@prefix_stack_trace(prefix=<your-prefix>)
def custom_prefix():
    ...
```

#### Implement `custom_message()`
By default, the exception message will be scrubbed and shown as "Exception message scrubbed". You can customize the message displayed with argument `scrub_message`:
```python
@prefix_stack_trace(scrub_message=<your-message>)
def custom_message():
    ...
```

#### Implement `keep_exception_message()`
While the exception message is scrubbed by default, you could also show it explicitly with the boolean argument `keep_message`:
```python
@prefix_stack_trace(keep_message=<a-boolean>)
def keep_exception_message():
    ...
```

#### Implement `keep_allowed_exceptions()`
Exception messages will be scrubbed unless the message or the exception type regex match one of the strings in the argument `allow_list`:
```python
@prefix_stack_trace(allow_list=[<your-allowed-exceptions>])
def keep_allowed_exceptions():
    ...
```

#### Implement `add_timestamp()`
You could also display the timestamp in your log using the boolean argument `add_timestamp`:
```python
@prefix_stack_trace(add_timestamp=<a-boolean>)
def add_timestamp():
    ...
```

### Submit your experiment

To submit your experiment with the parameter value defined in the config file, just run the command shown at the top of the experiment python file [demo_log_stack_trace_prefixing.py](../../shrike-examples/pipelines/experiments/demo_log_stack_trace_prefixing.py).

### Check the logs
Once your experiment has executed successfully, click on the component, then on "Outputs + logs". In the driver log (usually called "70_driver_log.txt"), you should see (by order)
- some logs prefixed with `<your-prefix>` for "ZeroDivisionError" with "Exception message scrubbed"
- A "SystemLog" for "ZeroDivisionError: SystemLog:" folloed by `<your-message>`
- A "SystemLog" with "ZeroDivisionError: SystemLog:division by zero"
- A "SystemLog" with timestamp and "ZeroDivisionError"

### Links to successful execution
A successful run of the experiment can be found [here](https://ml.azure.com/runs/531d46f7-0137-4996-9d34-fb2effbbe62b?wsid=/subscriptions/48bbc269-ce89-4f6f-9a12-c6f91fcb772d/resourcegroups/aml1p-rg/workspaces/aml1p-ml-wus2&tid=72f988bf-86f1-41af-91ab-2d7cd011db47). (This is mostly for internal use, as you likely will not have access to that workspace.)