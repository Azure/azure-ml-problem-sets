# Pipelines problem 03 - Consume a dataset

## Problem statement
Submit a single-component pipeline which consumes a dataset (for example count the number of records).

## Motivation
The goal of this problem is to get you familiar with how to read datasets as component inputs.

## Out of scope
_Outputting data_ is out of scope for this problem and will be covered in [problem 04](./pipelines-04.md).

## Prerequisites
To be able to consume a dataset, the main thing you need is, well, a dataset! If you do not have one already, you can create one from the Azure Open Datasets through the Azure ML UI, following [these instructions](https://docs.microsoft.com/en-us/azure/open-datasets/how-to-create-azure-machine-learning-dataset-from-open-dataset#create-datasets-with-the-studio).

## Guidance

### Prepare your component specification
Open the [component_spec.yaml](../../shrike-examples/components/count_rows/component_spec.yaml) file in the `components/count_rows` directory. Add an "`input_data`" integer parameter to the `inputs` section following the [CommandComponent documentation](https://componentsdk.azurewebsites.net/components/command_component.html), then add your newly added parameter to the command.


### Prepare your component script
The command in the component specification tells to run the [run.py](../../shrike-examples/components/count_rows/run.py) file located in the component folder. If you open this file, you will see that it just calls the main method of the [count_rows_script.py](../../shrike-examples/contoso/count_rows_script.py) file. It is _that_ file that we call the _component script_ and that we will now prepare.

#### Implement the `get_arg_parser()` method
First you need to implement a `get_arg_parser()` method that returns an instance of the argument parser. If you're not familiar with parsing arguments, the _argparse_ library [documentation](https://docs.python.org/3/library/argparse.html) should help. Here, we will have a single input named `input_data`.

#### Implement the `main()` method
Then, implement the `main()` method to read the dataset and count the number of rows. The name of the actual file to load depends on which dataset you're using - if you are unsure, just find your dataset in the UI and click "Explore"; it should tell you which files are available. 

After you've read the dataset (feel free to just use a sample if you have chosen a large dataset), count the number of rows and print the result. We suggest you use `pandas` for counting rows. As you can see in the [component_env.yaml](../../shrike-examples/components/count_rows/component_env.yaml) file that defines the environment where the component will run, `pandas` should be available.

### Configure your experiment
The various parameters controlling the execution of an experiment can be defined _via_ the _command line_, or _via_ a _configuration file_. In this problem, we will focus on the _configuration file_ route.
Open the experiment configuration file [demo_count_rows.yaml](../../shrike-examples/pipelines/config/experiments/demo_count_rows.yaml) that has already been prepared for you. Create a new section where you define the value of the `input_data` parameter, _i.e._ the name of your dataset. It should be similar to the below.

```yaml
# DemoComponent config
democomponent:
  input_data: <name-of-your-dataset> # the name of the dataset you'll be working on, as seen in the UI
  input_data_version: "latest" # this will ensure you always consume the latest version of the dataset
```

### Prepare your experiment python file
Now that your component should be ready and your experiment should be configured properly, let's prepare [your experiment python file](../../shrike-examples/pipelines/experiments/demo_count_rows.py). The process is very similar to what you did in in the previous problem. The main differences are as follows. 

- The pipeline function (`demo_pipeline_function()`) will now take an input dataset as an argument, that you will also need when instantiating the component.
- In the `pipeline_instance()` function, you will need to load the dataset using the name and version provided in the config file, and pass the loaded dataset to the pipeline function. 


### Submit your experiment

To submit your experiment with the parameter value defined in the config file, just run the command shown at the top of the experiment python file.

### Check the logs
Once your experiment has executed successfully, click on the component, then on "Outputs + logs". In the driver log (usually called "70_driver_log.txt"), look for the line containing the number of rows that you should have added in onf of the above steps. Tadaa!

### Links to successful execution
A successful run of the experiment can be found [here](https://ml.azure.com/runs/e50f9945-d9ec-417d-a593-0a4dbb6b7690?wsid=/subscriptions/48bbc269-ce89-4f6f-9a12-c6f91fcb772d/resourcegroups/aml1p-rg/workspaces/aml1p-ml-wus2&tid=72f988bf-86f1-41af-91ab-2d7cd011db47). (This is mostly for internal use, as you likely will not have access to that workspace.)