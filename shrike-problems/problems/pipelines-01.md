# Pipelines problem 01 - Hello, world!

## Problem statement
Submit a pipeline with a single "Hello, world!"-type component.

## Motivation
The goal of this problem is to get you familiar with how to use `shrike.pipeline` for creating and submitting experiments.

## Out of scope
_Component creation_ is out of scope for this problem and will be covered in [problem 02](./pipelines-02.md). For the current problem, we will be using the "Hello, world!" component defined in the `components/hello_world` folder - all it does is print "Hello, world!" in the logs.

## Guidance

### Set your workspace
Open the `pipelines/config/aml/public_workspace.yaml` file and update the `subscription_id`, `resource_group`, `workspace_name`, and `tenant` values with those corresponding to your workspace. You can get the first 3 by downloading the config file from the Azure ML UI (click on the workspace name in the top right, then on "Download config file"). You can get the last one (tenant Id) from the workspace URL (which should have a part like "_&tid=\<your-tenant-id\>_").

### Double check the computes and datastores names
Open the `pipelines/config/aml/public_workspace.yaml` file and double check that the `default_compute_target`, `linux_cpu_dc_target`, and `linux_cpu_prod_target` point to your cpu cluster (usually named "cpu-cluster" by default, but can be adjusted in this file if your cpu cluster has another name).

The `compliant_datastore` name should be the default "workspaceblobstore".

### Prepare the experiment python file
In Azure ML, the experiments (_a.k.a. graphs_) are typically defined _via_ code, in what we will call an "experiment python file". We have prepared a stub of this file for you: [demo_hello_world.py](../../shrike-examples/pipelines/experiments/demo_hello_world.py).

Open this file and start scrolling down. In the `HelloWorldDemo` class, you will first find a `build()` function, which first loads the subgraphs and components used in the graph (in our case, a single component). Look for the line below and insert the _component key_ that will control which component to load - you can find the component key in the components dictionary defined in the [module_defaults.yaml](../../shrike-examples/pipelines/config/modules/module_defaults.yaml) file.

```python
hello_world_component = self.component_load("<your-component-key>")
```

After that, keep scrolling and you will soon encounter the `demo_pipeline_function()` function which actually defines the graph. You can use the `name` and `description` parameters in the decorator to give a meaningful name and description to your graph. After that, we need to instantiate the components making up our graph. In our current, simple case of a 1-component graph, all we need is to instantiate a single step (`demo_component_step`) with the component we just loaded. To do so, just adjust the following line with the name of the component you loaded above.

```python
demo_component_step = name_of_component_loaded_above()
```

Finally, we leverage the `shrike.pipeline` package to apply the propoer run parameters (_e.g._ in which compute to run the component). To do so, just call the `apply_recommended_runsettings()` function as shown below, with the same component key you used to load the component; you can see how we specify this component to run on a cpu.

```python
self.apply_recommended_runsettings(
    "<your-component-key>", demo_component_step, gpu=False
)
```            

### Configure your experiment
The various parameters controlling the execution of an experiment can be defined _via_ the command line, or _via_ a _configuration file_
Open the experiment configuration file [demo_hello_world.yaml](../../shrike-examples/pipelines/config/experiments/demo_hello_world.yaml) that has already been prepared for you. Adjust the `run.experiment_name` parameter to give your experiment a meaningful name.

### Submit your experiment
To submit your experiment just run the command given at the top of the experiment [configuration file](../../shrike-examples/pipelines/config/experiments/demo_hello_world.yaml).

### Check the logs
Once your experiment has executed successfully, click on the component, then on "Outputs + logs". In the driver log (usually called "70_driver_log.txt"), look for the "Hello, world!" line. Tadaa!

### Links to successful execution
A successful run of the experiment can be found [here](https://ml.azure.com/runs/8043ce8a-5045-4211-9934-1959d5296a48?wsid=/subscriptions/48bbc269-ce89-4f6f-9a12-c6f91fcb772d/resourcegroups/aml1p-rg/workspaces/aml1p-ml-wus2&tid=72f988bf-86f1-41af-91ab-2d7cd011db47). (This is mostly for internal use, as you likely will not have access to that workspace.)
