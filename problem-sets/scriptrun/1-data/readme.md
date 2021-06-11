## Problem 1 - Local Data --> Cloud

Update:

1. **`azureml_upload.py`**
2. **`azureml_submit.py`**

### Outline

1. `azureml_upload.py`: Upload data to workspace default datastore.

    Use `ds = ws.get_default_datastore` method to get the datastore, and `ds.upload_files` method to upload
    local text file `wisdom.txt`.

2. `azureml_submit.py`: Create dataset and mount data to remote run.

    Read data from datastore in the remote run using an Azure ML dataset:
    - Create dataset `dataset = Dataset.File.from_files`
    - Pass as an argument to `ScriptRunConfig` like `arguments=["--data_dir", dataset.as_mount(), "--filename", "wisdom.txt"]`

**Note.** Observe that `wisdom.txt` is also uploaded as part of the snapshot. In this case we could have
simply read its contents from the current working directory by passing

```
arguments=["--data_dir", ".", "--filename", "wisdom.txt"]
```

However, this approach doesn't scale well as the snapshot size is limited.