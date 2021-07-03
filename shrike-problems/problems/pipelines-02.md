# Pipelines problem 02 - Component that operates on a parameter

## Problem statement
Submit a single-component pipeline where the component operates on a value passed as parameter (pass the parameter value through a config file or via the command line at pipeline submission time).

## Motivation
The goal of this problem is to get you familiar with how to create components that consumes parameters, and how to set parameter values.

## Out of scope
_Consuming a dataset_ is out of scope for this problem and will be covered in [problem 03](./pipelines-03.md).

## Guidance

### Prepare your component specification
Open the [component_spec.yaml](../../shrike-examples/components/add_one_thousand_to_parameter/component_spec.yaml) file in the `components/add_one_thousand_to_parameter` directory. Add a "`value`" integer parameter to the `inputs` section following the [CommandComponent documentation](https://componentsdk.azurewebsites.net/components/command_component.html), then add your newly added parameter to the command.

### Prepare your component script
The command in the component specification tells to run the [run.py](../../shrike-examples/components/add_one_thousand_to_parameter/run.py) file located in the component folder. If you open this file, you will see that it just calls the main method of the [add_one_thousand_to_parameter_script.py](../../shrike-examples/contoso/add_one_thousand_to_parameter_script.py) file. It is _that_ file that we call the _component script_ and that we will now prepare.

#### Implement the `get_arg_parser()` method
First you need to implement a `get_arg_parser()` method that returns an instance of the argument parser. If you're not familiar with parsing arguments, the _argparse_ library [documentation](https://docs.python.org/3/library/argparse.html) should help.

#### Implement the `main()` method
Then, implement the `main()` method to consume your newly introduced parameter. For this exercise, let's just add 1000 to the parameter value, and print both operands and the result.

### Add you component to the component dictionary
Open the [module_defaults.yaml](../../shrike-examples/pipelines/config/modules/module_defaults.yaml) file and add an entry for the new component following the example of the HelloWorldComponent.

- `key` is how you will retrieve the component later on.
- `name` must match the name you defined in the component specification.
- `yaml` is the location of the component specification.

### Configure your experiment
The various parameters controlling the execution of an experiment can be defined _via_ the _command line_, or _via_ a _configuration file_.
Open the experiment configuration file [demo_component_with_parameter.yaml](../../shrike-examples/pipelines/config/experiments/demo_component_with_parameter.yaml) that has already been prepared for you. Create a new section where you define the parameter value, something like the below.

```yaml
# DemoComponent config
democomponent:
  <your-parameter-name>: 314 # the value on which the component will operate
```

### Prepare your experiment python file
Now that your component should be ready and your experiment should be configured properly, let's prepare your experiment python file. The process is very similar to what you did in in the previous problem. The only difference is that when you instantiate your component, you will need to provide the parameter value defined in the config file, as demonstrated below.

```python
demo_component_step = component_with_parameter(<your-parameter-name> = config.democomponent.<your-parameter-name>)
```

### Submit your experiment...

#### ... with the parameter value defined in the config file
To submit your experiment with the parameter value defined in the config file, just run the command shown at the top of the experiment python file.

#### ... with the parameter value defined from the command line
To submit your experiment with the parameter value defined in the command line (and thus overriding the value in the config file), just run the command shown at the top of the experiment python file _with the following addition_.

```
democomponent.<your-parameter-name>=51
```

### Check the logs
Once your experiment has executed successfully, click on the component, then on "Outputs + logs". In the driver log (usually called "70_driver_log.txt"), look for the line starting with "The value passed as parameter is...". Tadaa!

### Links to successful execution
A successful run of the experiment can be found [here](https://ml.azure.com/runs/d8e205df-4351-406d-a1e2-8ffbea7b9741?wsid=/subscriptions/48bbc269-ce89-4f6f-9a12-c6f91fcb772d/resourcegroups/aml1p-rg/workspaces/aml1p-ml-wus2&tid=72f988bf-86f1-41af-91ab-2d7cd011db47). (This is mostly for internal use, as you likely will not have access to that workspace.)