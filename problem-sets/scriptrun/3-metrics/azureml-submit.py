from azureml.core import (
    Workspace,
    Experiment,
    Environment,
    ScriptRunConfig,
)

# get workspace
ws = Workspace.from_config()
target = ws.compute_targets['cpucluster']

# create environment
env = Environment.from_pip_requirements('pytorch-lightning', 'requirements.txt')

# set up script run configuration
config = ScriptRunConfig(
    source_directory='.',
    script='train.py',
    compute_target=target,
    environment=env,
)

# submit script to AML
exp = Experiment(ws, "aml-problem-set")
run = exp.submit(config)
run.set_tags({"problem": "2"})
print(run.get_portal_url()) # link to ml.azure.com
run.wait_for_completion(show_output=True, raise_on_error=True)
