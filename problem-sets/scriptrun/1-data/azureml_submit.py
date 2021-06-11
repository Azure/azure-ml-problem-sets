from azureml.core import (
    Dataset,
    Workspace,
    Experiment,
    ScriptRunConfig,
)

# connect to azureml assets
ws = Workspace.from_config()
target = ws.compute_targets["cpucluster"]

# create dataset
datastore = ws.get_default_datastore()
dataset = Dataset.File.from_files(path=(datastore, "azureml-problem-set/scriptrun-1"))

# set up script run configuration
config = ScriptRunConfig(
    source_directory='.',
    script='read_data.py',
    compute_target=target,
    arguments=["--data_dir", dataset.as_mount(), "--filename", "wisdom.txt"]
)

# submit script to AML
exp = Experiment(ws, "aml-problem-set")
run = exp.submit(config)
run.set_tags({"problem": "1"})
print(run.get_portal_url()) # link to ml.azure.com
run.wait_for_completion(show_output=True, raise_on_error=True)