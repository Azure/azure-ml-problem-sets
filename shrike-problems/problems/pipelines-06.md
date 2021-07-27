# Pipelines problem 06 - Dynamically generated graph
## Problem statement
Submit a pipeline where a component is chosen based on a parameter value.

## Motivation

In some cases, it can be useful to generate a graph on-the-fly, based on some parameter value. For instance, imagine a scenario where a data scientist has 2 different training components at her disposal, corresponding to 2 different model architectures. 
Having 2 distinct experiment python files whose sole difference is about the training component would lead to a lot of code duplication. Instead, it would be better to have a _single_ experiment python file, that has the ability to switch between the 2 training modules based on some parameter value.

It is possible to do exactly this with shrike. This problem will illustrate this concept on a simplified use case: a single-component pipeline, for which the component is chosen based on a parameter value. Namely, if the parameter value is "helloworld", we will use the "Hello, World!" component from problem 01; if the parameter value is "democomponent", we will use the demo component from problem 02.

## Prerequisites
You need to have solved [problem 01](./pipelines-01.md) and [problem 02](./pipelines-02.md), as we will be using the components introduced in those problems.

## Guidance

### Configure your experiment

A stub for your experiment config file has been created: [demo_dynamic_graph.yaml](../../shrike-examples/pipelines/config/experiments/demo_dynamic_graph.yaml). You will need to add 2 parameters to this config file.

- `which_component` for controlling which component to use. Provide "*helloworld*" as default value, and put it in its own section for clarity (we recommend `dynamicgraphparameter` as a section name).
- `value` for choosing what value to operate on, in the case where the demo component is executed. Provide an integer default value, and put it in its own section for clarity (we recommend `democomponent` as a section name).

### Prepare your experiment python file

Now we are going to prepare the experiment python file, which will contain the logic for choosing the component based on a parameter value. What you will do is very similar to what you did in the first few problems; the main difference is that we'll use an `if` block to instantiate the components.

Open the [demo_dynamic_graph.py](../../shrike-examples/pipelines/experiments/demo_dynamic_graph.py) file that has been prepared for you. First, you will want to load *both* components in the build function, since at this stage we don't know yet which one we'll be using.

Then, in the `demo_pipeline_function()`, you will need to create a variable containing the parameter value as found in the config file. If you followed the naming suggestions above, that would mean adding a line like below.

```python
which_component = config.dynamicgraphparameter.which_component
```

Now you should use this newly introduced variable to implement the following logic. If the variable value is "*helloworld*", instantiate the "Hello, World!" component from problem 01; if the variable value is "*democomponent*", instantiate the demo component from problem 02 (in this case, you'll also need to provide a parameter value from the config file).

Remember that in both cases you will need to call `apply_recommended_runsettings()` after instantiating the component.

After all this, your experiment python file should be ready for submission.

### Submit your experiments

To submit your first experiment, just run the command shown at the top of the experiment python file, which is also pasted below for convenience.

```ps1
python pipelines/experiments/demo_dynamic_graph.py --config-dir pipelines/config --config-name experiments/demo_dynamic_graph run.submit=True
```

This will submit the experiment with the value of the `which_component` parameter defined in the [experiment config file](../../shrike-examples/pipelines/config/experiments/demo_dynamic_graph.yaml), so if you followed the above instructions, the "Hello, World!" component should be used.

Now, let's try to change the value of `which_component` to use the demo component from problem 02. One way to do this is to directly change the value in the config file and re-run the command above as-is. Another way is to override the parameter value in the command line (when using shrike, command-line parameter definitions will always override parameter definitions through config file). To do so, just add the following to the command above (assuming you followed the naming suggested in the above sections).

```ps1
dynamicgraphparameter.which_component="democomponent"
```

### Check the experiments

Once your two experiments have been submitted successfully, find them in the UI and check what component was used.

### Links to successful executions

Successful runs of the experiment can be found [here](https://ml.azure.com/runs/161935ea-acdf-4942-8941-1cecee284ed6?wsid=/subscriptions/48bbc269-ce89-4f6f-9a12-c6f91fcb772d/resourcegroups/aml1p-rg/workspaces/aml1p-ml-wus2&tid=72f988bf-86f1-41af-91ab-2d7cd011db47) and [there](https://ml.azure.com/runs/d2f572e6-61d5-49d5-8ca4-9a23d1d23812?wsid=/subscriptions/48bbc269-ce89-4f6f-9a12-c6f91fcb772d/resourcegroups/aml1p-rg/workspaces/aml1p-ml-wus2&tid=72f988bf-86f1-41af-91ab-2d7cd011db47). (These are mostly for internal use, as you likely will not have access to that workspace.)