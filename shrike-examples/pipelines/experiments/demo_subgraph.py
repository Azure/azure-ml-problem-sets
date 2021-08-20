"""
The Azure ML pipeline for running a graph that includes a subgraph.

to execute:
> python pipelines/experiments/demo_subgraph.py --config-dir pipelines/config --config-name experiments/demo_subgraph run.submit=True
"""
# pylint: disable=no-member
# NOTE: because it raises 'dict' has no 'outputs' member in dsl.pipeline construction
import os
import sys

from azure.ml.component import dsl
from shrike.pipeline.pipeline_helper import AMLPipelineHelper

# NOTE: if you need to import from pipelines.*
ACCELERATOR_ROOT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
if ACCELERATOR_ROOT_PATH not in sys.path:
    print(f"Adding to path: {ACCELERATOR_ROOT_PATH}")
    sys.path.append(str(ACCELERATOR_ROOT_PATH))

# import any subgraph you might need in self.required_subgraphs()
from pipelines.subgraphs.probesubgraph import DemoSubgraph


class DemoGraphWithSubgraph(AMLPipelineHelper):
    """Runnable/reusable pipeline helper class

    This class inherits from AMLPipelineHelper which provides
    helper functions to create reusable production pipelines for Accelerator Demo.
    """

    @classmethod
    def required_subgraphs(cls):
        """Declare dependencies on other subgraphs to allow AMLPipelineHelper to build them for you.

        This method should return a dictionary:
        - Keys will be used in self.subgraph_load(key) to build each required subgraph.
        - Values are classes inheriting from AMLPipelineHelper

        Returns:
            dict[str->AMLPipelineHelper]: dictionary of subgraphs used for building this one.
        """
        return {"DemoSubgraph": DemoSubgraph}

    def build(self, config):
        """Builds a pipeline function for this pipeline using AzureML SDK (dsl.pipeline).

        This method returns a constructed pipeline function (decorated with @dsl.pipeline).

        Args:
            config (DictConfig): configuration object

        Returns:
            dsl.pipeline: the function to create your pipeline
        """

        # helper functions below load the subgraph/component from registered or local version depending on your config.run.use_local
        probe_subgraph = self.subgraph_load("DemoSubgraph")

        # Here you should create an instance of a pipeline function (using your custom config dataclass)
        @dsl.pipeline(
            name="demo-eyesoff",
            description="The AML eyes-off pipeline using a subgraph with the Probe component for Accelerator Demo",
            default_datastore=config.compute.compliant_datastore,
        )
        def demo_pipeline_function(probe_dataset):
            """Pipeline function for this graph.

            Args:
                probe_dataset (TabularDataset): input dataset (usually obtained through extraction from Heron portal)

            Returns:
                dict[str->PipelineOutputData]: a dictionary of your pipeline outputs
                    for instance to be consumed by other graphs
            """
            # general syntax:
            # component_instance = component_class(input=data, param=value)
            # or
            # subgraph_instance = subgraph_function(input=data, param=value)

            N_subgraphs = 3
            subgraphs = []

            subgraph_1 = probe_subgraph(
                probe_dataset=probe_dataset,
                param_scan_args=config.probesubgraph.scan_args,
                param_scan_deps=config.probesubgraph.scan_deps,
                param_scan_input=config.probesubgraph.scan_input,
                param_scan_env_1=config.probesubgraph.scan_env_1,
                param_scan_env_2=config.probesubgraph.scan_env_2,
                param_verbose=config.probesubgraph.verbose,
            )

            subgraphs.append(subgraph_1)

            for ind in range(1, N_subgraphs):
                subgraph = probe_subgraph(
                    probe_dataset=subgraphs[ind - 1].outputs.subgraph_results,
                    param_scan_args=config.probesubgraph.scan_args,
                    param_scan_deps=config.probesubgraph.scan_deps,
                    param_scan_input=config.probesubgraph.scan_input,
                    param_scan_env_1=config.probesubgraph.scan_env_1,
                    param_scan_env_2=config.probesubgraph.scan_env_2,
                    param_verbose=config.probesubgraph.verbose,
                )

                subgraphs.append(subgraph)

            return {"subgraph_results": subgraphs[N_subgraphs - 1].outputs.subgraph_results}


        # finally return the function itself to be built by helper code
        return demo_pipeline_function

    def pipeline_instance(self, pipeline_function, config):
        """Given a pipeline function, creates a runnable instance based on provided config.

        This is used only when calling this as a runnable pipeline using .main() function (see below).
        The goal of this function is to map the config to the pipeline_function inputs and params.

        Args:
            pipeline_function (function): the pipeline function obtained from self.build()
            config (DictConfig): configuration object

        Returns:
            azureml.core.Pipeline: the instance constructed with its inputs and params.
        """
        # NOTE: self.dataset_load() helps to load the dataset based on its name and version
        pipeline_input_dataset = self.dataset_load(
            name=config.probesubgraph.input_data,
            version=config.probesubgraph.input_data_version,
        )

        # when all inputs are obtained, we call the pipeline function
        probe_pipeline = pipeline_function(probe_dataset=pipeline_input_dataset)

        # and we return that function so that helper can run it.
        return probe_pipeline


# NOTE: main block is necessary only if script is intended to be run from command line
if __name__ == "__main__":
    # calling the helper .main() function
    DemoGraphWithSubgraph.main()
