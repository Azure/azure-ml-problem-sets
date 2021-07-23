# Pipelines problem 05 - Use a subgraph

## Problem statement
Submit a multi-component pipeline which uses a subgraph.

## Motivation

When several components are reused in the same fashion across multiple graphs, it is good practice to group these components into a _subgraph_, that can be reused more easily than the individual components. Using subgraphs avoids code duplication, and facilitates code reuse. 

This problem builds upon [problem 04](./pipelines-04.md). It will teach you how to create and use a basic _subgraph_ that encapsulates the 2 `probe` components that we chained together in problem 4.

## Prerequisites
You need to have solved [problem 04](./pipelines-04.md).

## Guidance

### Configure your experiment

The config file for your experiment [demo_subgraph.yaml](../../shrike-examples/pipelines/config/experiments/demo_subgraph.yaml) has already been prepared. All you need to do is adjust the name of the input dataset to the one available in your workspace.

Please note how it differs from the config file we used in problem 4. Here, all the parameters for the 2 `probe` components are defined in a single section called "probesubgraph", which also contains the input parameters. This will be important when we try to refer to these parameters in the experiment python file.

Also note that since we're deciding only the `scan_env` parameter will have a different value between the 2 components, we do not need to duplicate all other parameters.

### Prepare your subgraph python file

First we are going to define our subgraph in its own python file. The easiest way to proceed is to start with the experiment file from problem 4: [demo_chain_components.py](../../shrike-examples/pipelines/experiments/demo_chain_components.py). Take this file, copy it into a `pipelines/subgraphs` folder, and rename it [probesubgraph.py](../../shrike-examples/pipelines/subgraphs/probesubgraph.py).

The first thing you need to do is rename the class. Something like "DemoSubgraph" should be appropriate.

After that, let's deal with the `demo_pipeline_function()` function. First, let's rename it to something like `demosubgraph_pipeline_function`. Then we need to give it arguments (we won't be able to call the config file directly from this function; instead, we will call it from the experiment python file, and will pass the parameters to the subgraph). Just add, after `probe_dataset`, the other arguments that can be found in the "probesubgraph" section of the config file To avoid confusion, rename them by prefixing them with "param_". Give them a default value.

Next, when instantiating the 2 components, use your newly added parameters instead of the values from the config file.

Finally, since this subgraph is not meant to be run on its own (just as part of a larger graph), we can delete the `pipeline_instance()` function and the main block.

### Prepare your experiment python file

Now we are going to prepare the experiment python file, which will call the subgraph we just defined.

This is very similar to what you did in the first few problems; the main difference is that instead of creating a graph with a single _component_, you will create a graph with a single _subgraph_.

Open the [demo_subgraph.py](../../shrike-examples/pipelines/experiments/demo_subgraph.py) that has been prepared for you. First , you will want to import the subgraph. If you followed the naming suggestions in the above section, you should need a line like what follows.

```python
from pipelines.subgraphs.probesubgraph import DemoSubgraph
```

The next step has been implemented for you already, but please check out the `required_subgraphs()` function. This is where you would declare which subgraphs are going to be used. If you were to use more (or different) subgraphs, they would be added to the dictionary returned by this function. See the function docstring for more detailed explanations.

After that, it is time to load the subgraph in the `build()` function. Instead of using `component_load(ComponentKey)`, we'll use the analogous `subgraph_load(SubgraphKey)`. Adjust the corresponding line accordingly.

Finally, we need to prepare the `demo_pipeline_function()` by instantiating the probe subgraph and providing the parameter values from the config files. Again, this is fairly analogous to what we were doing in the first few problems when instantiating individual components. The difference here is that we do not need to call `apply_recommended_runsettings()` because this has already been done in the subgraph file.

### Submit your experiment

To submit your experiment, just run the command shown at the top of the experiment python file.

### Check the logs

Once your experiment has executed successfully, click on one of the `probe` components, then on "Outputs + logs". In the driver log (usually called "70_driver_log.txt"), look for the lines describing the size and number of input files. See how these lines differ between the 2 successive components. Tadaa!

> Remark: the Azure ML UI does not treat the subgraphs in any special way (for now), so the graph will look exactly the same as the one from the previous problem; there is no grouping of components happening in the UI, all the components making up the subgraph are displayed.

### Links to successful execution

A successful run of the experiment can be found [here](https://ml.azure.com/runs/aa87d57b-f2f5-4dcb-8ba1-b7dc54bc9031?wsid=/subscriptions/48bbc269-ce89-4f6f-9a12-c6f91fcb772d/resourcegroups/aml1p-rg/workspaces/aml1p-ml-wus2&tid=72f988bf-86f1-41af-91ab-2d7cd011db47). (This is mostly for internal use, as you likely will not have access to that workspace.)