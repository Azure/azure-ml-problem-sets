# Problem set for ramping up on the _shrike_ package 

## Contents
This document is a proposal of a list of problems to help people learn how to use [shrike](https://github.com/azure/shrike).

## List of problems

:warning: Note that these problems are meant to be tackled sequentially, as the solution of problem _N+1_ builds upon the solution of problem _N_.

### Creating, submitting, and validating pipelines

- [Pipelines Problem 01](./problems/pipelines-01.md) Submit a pipeline with a single "Hello, world!"-type component.
- [Pipelines Problem 02](./problems/pipelines-02.md) Submit a single-component pipeline where the component operates on a value passed as parameter (pass the parameter value through a config file or via the command line at pipeline submission time).
- [Pipelines Problem 03](./problems/pipelines-03.md) Submit a single-component pipeline which consumes a dataset (for example count the number of records).
- [Pipelines Problem 04](./problems/pipelines-04.md) Submit a multi-component pipeline where one component's output is the input of a subsequent component.
- [Pipelines Problem 05](./problems/pipelines-05.md) Submit a multi-component pipeline which uses a subgraph.
- [Pipelines Problem 06](./problems/pipelines-06.md) Submit a pipeline where a component is chosen based on a parameter value.
- [Pipelines Problem 07](./problems/pipelines-07.md) Add integration tests to ensure a pipeline does not break.

### Logging

:construction: Work in Progress :construction:

- [Logging Problem 01](./problems/logging-01.md) Submit a pipeline using the compliant logger to log various properties of the dataset consumed by a component (such as number of records or average of a numerical field, for instance).
- [Logging Problem 02](./problems/logging-02.md) Experiment with the different data categories available to the compliant logger.
- [Logging Problem 03](./problems/logging-03.md) Experiment with the various options about stack trace prefixing (customize the prefix and the exception message, scrub the exception message unless it is in an allowed list).
