"""
The AML pipeline for the eyes-off demo graph

to execute:
> python pipelines/experiments/demo_chain_components.py --config-dir pipelines/config --config-name experiments/demo_chain_components run.submit=True
"""
# pylint: disable=no-member
# NOTE: because it raises 'dict' has no 'outputs' member in dsl.pipeline construction
import os
import sys
from dataclasses import dataclass
from typing import Optional

from azure.ml.component import dsl
from shrike.pipeline.pipeline_helper import AMLPipelineHelper

# NOTE: if you need to import from pipelines.*
ACCELERATOR_ROOT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
if ACCELERATOR_ROOT_PATH not in sys.path:
    print(f"Adding to path: {ACCELERATOR_ROOT_PATH}")
    sys.path.append(str(ACCELERATOR_ROOT_PATH))


class ChainComponentsDemo(AMLPipelineHelper):
    """Runnable/reusable pipeline helper class

    This class inherits from AMLPipelineHelper which provides
    helper functions to create reusable production pipelines.
    """

    def build(self, config):
        """Builds a pipeline function for this pipeline using AzureML SDK (dsl.pipeline).

        This method returns a constructed pipeline function (decorated with @dsl.pipeline).

        Args:
            config (DictConfig): configuration object

        Returns:
            dsl.pipeline: the function to create your pipeline
        """

        # helper functions below load the subgraph/component from registered or local version depending on your config.run.use_local
        probe_component = self.component_load("probe")

        # Here you should create an instance of a pipeline function (using your custom config dataclass)
        @dsl.pipeline(
            name="demo-chain-components",
            description="The Azure ML demo of a graph where components are chained, i.e. the input of a component is the output of an upstream component.",
            default_datastore=config.compute.compliant_datastore,
        )
        def demo_pipeline_function(probe_dataset):
            """Pipeline function for this graph.

            Args:
                probe_dataset (FileDataset): input dataset (usually obtained through extraction from Heron portal)

            Returns:
                dict[str->PipelineOutputData]: a dictionary of your pipeline outputs
                    for instance to be consumed by other graphs
            """
            # general syntax:
            # module_instance = module_class(input=data, param=value)
            # or
            # subgraph_instance = subgraph_function(input=data, param=value)
            probe_component_step_1 = probe_component(
                input_data=probe_dataset,
                scan_args=config.probe1.scan_args,
                scan_deps=config.probe1.scan_deps,
                scan_input=config.probe1.scan_input,
                scan_env=config.probe1.scan_env,
                verbose=config.probe1.verbose,
            )

            self.apply_recommended_runsettings(
                "probe", probe_component_step_1, gpu=True
            )

            probe_component_step_2 = probe_component(
                input_data=probe_component_step_1.outputs.results,  # this is where we pipe the output of the first module to the input of the second module
                scan_args=config.probe2.scan_args,
                scan_deps=config.probe2.scan_deps,
                scan_input=config.probe2.scan_input,
                scan_env=config.probe2.scan_env,  # here we're using a different parameter
                verbose=config.probe2.verbose,
            )

            self.apply_recommended_runsettings(
                "probe", probe_component_step_2, gpu=True
            )

            # return {key: output}
            return {"subgraph_results": probe_component_step_2.outputs.results}

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
            name=config.inputs.input_data,
            version=config.inputs.input_data_version,
        )

        # when all inputs are obtained, we call the pipeline function
        probe_pipeline = pipeline_function(probe_dataset=pipeline_input_dataset)

        # and we return that function so that helper can run it.
        return probe_pipeline


# NOTE: main block is necessary only if script is intended to be run from command line
if __name__ == "__main__":
    # calling the helper .main() function
    ChainComponentsDemo.main()
