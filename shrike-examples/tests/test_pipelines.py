"""
PyTest suite for testing all runnable pipelines.
"""

import sys
from unittest.mock import patch

from pipelines.experiments.demo_subgraph import DemoGraphWithSubgraph

### Pipeline validation tests (integration tests)

def test_demo_subgraph_build_local(pipeline_config_path="pipelines/config"):
    """ Tests the subgraph demo graph by running the main function itself (which does .validate()) """
    testargs = [
        "prog",
        "--config-dir",
        pipeline_config_path,
        "--config-name",
        "experiments/demo_subgraph",
        "module_loader.use_local='*'",
    ]
    # will do everything except submit :)
    with patch.object(sys, "argv", testargs):
        DemoGraphWithSubgraph.main()
