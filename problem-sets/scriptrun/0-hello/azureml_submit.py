from azureml.core import (
    Workspace,
    Experiment,
    ScriptRunConfig,
)

# connect to azureml assets
ws = Workspace.from_config()
target = ws.compute_targets["cpucluster"]

# set up script run configuration
config = ScriptRunConfig(
    source_directory='.',
    script='hello.py',
    compute_target=target,
)

# submit script to AML
exp = Experiment(ws, "aml-problem-set")
run = exp.submit(config)

run.set_tags({"problem": "0"})
print(run.get_portal_url()) # link to ml.azure.com
run.wait_for_completion(show_output=True, raise_on_error=True)