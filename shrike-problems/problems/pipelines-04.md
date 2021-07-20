# Pipelines problem 04 - Chain components

## Problem statement
Submit a multi-component pipeline where one component's output is the input of a subsequent component.

## Motivation
The goal of this problem is to get you familiar with how to chain components together, _i.e._ use the output of a component as the input of another downstream component. 

To achieve this, we will be leveraging the `probe` component that can be found in the `components/probe` directory. This component lists various properties of the environment where it is executed (such as the available packages and their versions, the environment variables...), along with the number and size of input files. All this information is written in an output file, which can then be used as the input of another instance of the `probe` component

## Out of scope
_Grouping components_ into _subgraphs_ is out of scope for this problem and will be covered in [problem 05](./pipelines-05.md).

## Prerequisites
You need to be familiar with how to build and submit basic pipelines, and you ned to have a dataset available for consumption in your Azure ML workspace. If you have already solved the previous problems, you should be good to go.

## Guidance

We will keep this problem short and to the point. The `probe` component has already been implemented, so we will focus on how to _chain the components_.

### Configure your experiment

The config file for your experiment [demo_chain_components.yaml](../../shrike-examples/pipelines/config/experiments/demo_chain_components.yaml) has already been prepared. All you need to do is adjust the name of the input dataset to the one available in your workspace

### Prepare your experiment python file

Now, let's prepare [your experiment python file](../../shrike-examples/pipelines/experiments/demo_chain_components.py). The process is very similar to what you did in in the previous problems. 

You will see that the 2 probe components have been instantiated in the `demo_pipeline_function()` function. All that is left to do is to actually "pipe" the output of the first probe component to the input of the second one. In other words, all we need to do is "draw the arrow" to connect the 2 components.

This is very easy to do. When instantiating the second component, for the input data you want something like below.
```python
input_data=probe_component_step_1.outputs.<name-of-output-to-pipe>
```

You can find the `<name-of-output-to-pipe>` in the probe component specification.

### Submit your experiment

To submit your experiment, just run the command shown at the top of the experiment python file.

### Check the logs

Once your experiment has executed successfully, click on one of the `probe` components, then on "Outputs + logs". In the driver log (usually called "70_driver_log.txt"), look for the lines describing the size and number of input files. See how these lines differ between the 2 successive components. Tadaa!

### Links to successful execution

A successful run of the experiment can be found [here](https://ml.azure.com/experiments/id/b04a0674-7958-4627-8f10-04a85f29a112/runs/f3c42ff6-e69f-44cb-8d0e-d1842e847d3d?wsid=/subscriptions/48bbc269-ce89-4f6f-9a12-c6f91fcb772d/resourcegroups/aml1p-rg/workspaces/aml1p-ml-wus2&tid=72f988bf-86f1-41af-91ab-2d7cd011db47). (This is mostly for internal use, as you likely will not have access to that workspace.)