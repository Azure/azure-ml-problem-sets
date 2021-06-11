import numpy as np

is_remote_run = False
try:
    from azureml.core.run import Run, _OfflineRun
    run = Run.get_context()
    if not isinstance(run, _OfflineRun):
        print(f"Remote run detected")
        is_remote_run = True
except:
    print(f"No remote run detected")

xs = []
ys = []