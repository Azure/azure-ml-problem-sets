# Pipelines problem 07 - Integration tests for pipelines
## Problem statement
Add integration tests to ensure a pipeline does not break.

## Motivation

A simple change in a single component can have a huge impact on your team's experiments. Even a trivial change, if not carefully tested, can break the component. This results in whole pipelines being broken, which slows down your coworkers and requires resources to investigate and debug.

Using shrike, it is possible to create *integration tests for your pipelines*. Passing these tests will not guarantee that your pipeline does what it is supposed to do, but at least it will ensure that your pipeline can be *submitted* for execution (which wouldn't be the case, for instance, if there's a breaking change about the component interface).

This problem will show you how to add integration tests for your pipelines.

## Prerequisites
You need to have solved [problem 05](./pipelines-05.md), since we will be testing the pipeline introduced in this problem.

## Guidance

### Python file for pipelines integration tests

The basic idea behind these integration tests is fairly simple: call the _main()_ method of a pipeline without actually submitting it, and use local versions of all modules. Under the hood, shrike calls the `validate()` SDK method, which does the heavy lifting of validating that the pipeline can be submitted. If you didn't change the default `False` value of the `run.submit` parameters for the problems above, then shrike will not submit your experiment - which is what we want for these integration tests. 

All of this is fairly straightforward to do. Start by opening the [tests/test_pipelines.py](../../shrike-examples/tests/test_pipelines.py).

First, you will need to import the class corresponding to the pipeline you want to test. For the problem 05 subgraph, if you followed our suggested naming it should be something like:

```python
from pipelines.experiments.demo_subgraph import DemoGraphWithSubgraph
```

Then you will need to modify the test arguments to point to the config file for your experiment, and to load the default version of all modules.

Finally, just call the main method of your pipeline with your overridden test arguments. 

### Run the tests

To run the tests, use the command below. If you have completed problem 05 and followed the instructions above, the test should just pass.

```ps1
pytest .\tests\test_pipelines.py -v
```

### Possible follow-ups

#### Add other pipelines to the test file

One possible follow-up would be to add other pipelines to these tests. Just follow the pattern in the test file to add more. Notice how you can set different parameter values for testing different flavors of a pipeline (this would be useful for testing the 2 flavors of the dynamic graph introduced in problem 06).

#### Treat integration tests as gatekeepers

To ensure no change breaks existing pipelines, **we strongly recommend to treat these integration tests as gatekeepers and make them required for any PR to be merged**. To do so in DevOps, just include an extra `pytest` step in your build pipeline to run all relevant tests. An example can be found [here](https://dev.azure.com/msdata/Vienna/_git/aml-ds?path=%2Frecipes%2Fcompliant-experimentation%2Fazure-pipelines.yml&version=GBmain&line=38&lineEnd=46&lineStartColumn=1&lineEndColumn=35&lineStyle=plain&_a=contents); note how you will need to use a service connection to ensure the build agent has the required permissions to validate the experiment.





