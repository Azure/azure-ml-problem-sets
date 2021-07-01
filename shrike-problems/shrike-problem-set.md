# Problem set for ramping up on the _shrike_ package 

## Contents
This document is a proposal of a list of problems to help people learn how to use [shrike](https://github.com/azure/shrike).

## List of problems

### Creating, submitting, and validating pipelines

1. Submit a pipeline with a single "Hello, World!"-type component.
2. Submit a single-component pipeline where the component operates on a value passed as parameter (pass the parameter value through a config file or via the command line at pipeline submission time).
3. Submit a single-component pipeline which consumes a dataset (for example count the number of records).
4. Submit a multi-component pipeline where one component's output is the input of a subsequent component.
5. Submit a multi-component pipeline which uses a subgraph.
6. Submit a pipeline where a component is chosen based on a parameter value.
7. Re-submit one of the previous pipelines but with a different component version.
8. Add integration tests to ensure a pipeline does not break.

### Logging

1. Submit a pipeline using the compliant logger to log various properties of the dataset consumed by a component (such as number of records or average of a numerical field, for instance).
2. Experiment with the different data categories available to the compliant logger.
3. Experiment with the various options about stack trace prefixing (customize the prefix and the exception message, scrub the exception message unless it is in an allowed list).
