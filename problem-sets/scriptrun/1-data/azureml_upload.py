from azureml.core import Workspace

from azureml.core import Workspace

ws = Workspace.from_config()
ds = ws.get_default_datastore()

ds.upload_files(
    ["./wisdom.txt"],
    target_path="azureml-problem-set/scriptrun-1",
    overwrite=True,
)