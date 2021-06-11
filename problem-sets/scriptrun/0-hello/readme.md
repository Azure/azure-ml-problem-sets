## Problem 0 - Hello, World!

Update **`azureml_submit.py`**.

### Outline

1. Download the azureml-sdk. Example, using conda and python 3.8:

    ```bash
    conda create -n azureml python=3.8 pip -y
    connda activate azureml
    pip install azureml-sdk
    python -c "import azureml.core; print(azureml.core.__version__)"
    ```

2. Either create a **workspace** and **compute target** or use a shared workspace / cluster.

    **Note.** You can create the workspace from the [Azure Portal](https://ms.portal.azure.com/#home) or [via the SDK](https://azure.github.io/azureml-cheatsheets/docs/cheatsheets/python/v1/installation).

    Either way, you should have a workspace you are able to connect to with

    ```python
    from azureml.core import Workspace
    ws = Workspace(
        subscription_id="<subscription_id>",
        resource_group="<resource_group>",
        workspace_name="<workspace_name>",
    )
    ```

    and a compute target you are able to connect with

    ```python
    target = ws.compute_targets["<target-name>"]
    ```

3. Create submission script `azureml_submit.py` that:

    1. Connects to the workspace
    2. Grabs a (small!) compute target
    3. Creates a `ScriptRunConfig`
    4. Creates an experiment
    5. Submits the run

    See [azureml-cheatsheet/running-code-in-the-cloud](https://azure.github.io/azureml-cheatsheets/docs/cheatsheets/python/v1/script-run-config) for details.