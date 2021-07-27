"""
PyTest suite for testing all runnable pipelines.
"""

import sys
from unittest.mock import patch

# To-Do: import your pipeline class

### Pipeline validation tests (integration tests)

def test_demo_subgraph_build_local(pipeline_config_path="pipelines/config"):
    """ Tests the subgraph demo graph by running the main function itself (which does .validate()) """
    testargs = [
        "prog",
        "--config-dir",
        pipeline_config_path,
        "--config-name",
        "experiments/<YourExperimentConfigFile>", # To-Do: point to the right config file
        "module_loader.use_local='<ComponentKey>'", # To-Do: make sure the local version is used for ALL components - '*' could be helpful here
    ]
    # will do everything except submit :)
    with patch.object(sys, "argv", testargs):
        # To-Do: call the main method of your pipeline
