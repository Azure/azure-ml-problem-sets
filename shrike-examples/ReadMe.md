## Getting started with the `shrike` problems

### Prerequisites
- Provision a public AML workspace (you can find instructions [here](https://docs.microsoft.com/en-us/azure/machine-learning/concept-workspace#-create-a-workspace)).
    - Note that you do NOT want a Heron _a.k.a._ eyes-off _a.k.a._ compliant workspace. This introductory problem set is fairly general and does not touch on compliance-specific notions, so using a Heron workspace would make things more complicated.
- Create a dataset of type `FileDataset` (as opposed to `TabularDataset`).
    - This can be done following [these instructions](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-connect-data-ui#create-datasets). You can create a dataset from a local csv on your machine, [this iris.csv file](https://gist.github.com/netj/8836201) for instance (just download it first, from the link above, then upload it to your workspace as you create the dataset). 


### Setup


- Clone the current repository and set `shrike-examples` as your working directory.
- Set up and activate a new Conda environment:
  `conda create --name shrike-examples-env python=3.7 -y`,
  `conda activate shrike-examples-env`.
- Install the `shrike` dependencies:
  `pip install -r requirements.txt`

## List of problems

The list of problems is given [here](../shrike-problems/shrike-problem-set.md) in the
`shrike-problems` directory, and guidance for individual problems can be found in the
`problems` subdirectory. 

To solve the problems, just follow the **Guidance** section in each problem description,
and modify the appropriate files as indicated. You can look for the `# To-Do` comment string to locate the parts of the files that need modifying.