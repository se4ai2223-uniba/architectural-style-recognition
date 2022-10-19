
# Version Control and Experiment Tracking

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Introduction](#introduction)
  - [Why Reproducibility?](#why-reproducibility)
  - [Data versioning, Pipeline and Experiment Tracking](#data-versioning-pipeline-and-experiment-tracking)
  - [Technologies: DVC, MLFlow, DagsHub](#technologies-dvc-mlflow-dagshub)
- [Intermediate Steps](#intermediate-steps)
  - [Setting Up DugsHub](#setting-up-dugshub)
  - [Code restructuring](#code-restructuring)
- [DVC](#dvc)
- [MLFlow](#mlflow)
  - [Parameters](#parameters)
  - [Metrics](#metrics)



## Introduction

### Why Reproducibility?

Reproducibility is essential for an experiment in any domain.
The authors of an experiment have to document every aspect of it in order to make it possible for other people to do it again in the same conditions and verify if they obtains the same results.
This obviously also applies in the machine learning domain.

### Data Versioning, Pipeline and Experiment Tracking

Using data versioning we can track and store changes in data over time, this allows to load the proper data used in a certain experiment done at time t.
Using a pipeline we can establish an unique sequence of actions in order to reproduce the experiment without any variation in the order of steps.
Using experiment tracking we can store the results of any experiment, usually we want to store the hypeparameters and the metrics of a certain run.

### Technologies: DVC, MLFlow, DagsHub
In this project DVC is used for data versioning and for the implementation of the pipeline, then MLFlow is used for experiment tracking.DagsHub has been adopted as storage for DVC and as hub for MlFlow having an unique place for our reproducibility tasks.


## Intermediate steps

### Setting up DagsHub


### Code Restructuring

In order to conform to the standard structure of a machine learning pipeline, we moved the original code from the original ipynb notebook to three different python files, corresponding to the three main steps of the pipeline.


[![pipeline-files.png](https://i.postimg.cc/pLPB6YkN/pipeline-files.png)](https://postimg.cc/zVPWLh9p)





## DVC

The dvc.yaml is divided into three stages, corresponding to the phases of our machine learning pipeline: data preparation, training and prediction. 
To each stage is associated:
<ul>
    <li> a python file, containing the code to be executed in that phase </li>
    <li> the dependencies required for the execution of the stage </li>
    <li> the output files generated at the end of the stage </li>
</ul>

A graph representing the summary of our dvc pipeline is reported below:

[![eb58fef3-5ecb-4fb3-bb94-794513ba69a0.jpg](https://i.postimg.cc/rmn8BLB6/eb58fef3-5ecb-4fb3-bb94-794513ba69a0.jpg)](https://postimg.cc/47ckcj4w)





## MLFlow

We have tracked parameters and metrics relevant to our ML model using MLFlow, by writing the appropriate code in the file train_model.py. The results are visible in our DagsHub repository under the "Experiments" tab. Below we report the relevant code and the visualization in MLFlow of our parameters and our metrics (derived from two different experiments).

### Parameters

[![params-code.png](https://i.postimg.cc/66GvKjQs/params-code.png)](https://postimg.cc/ThfwqcmQ)

[![params-mlflow.png](https://i.postimg.cc/FFjHG2RK/params-mlflow.png)](https://postimg.cc/hhtntZVF)


### Metrics

[![metrics-code.png](https://i.postimg.cc/HkKmT2xK/metrics-code.png)](https://postimg.cc/PCm9411z)

[![metrics-mlflow-1.png](https://i.postimg.cc/PqZgTn0p/metrics-mlflow-1.png)](https://postimg.cc/VSfGWpfm)

[![metrics-mlflow-2.png](https://i.postimg.cc/mrQ5KNF7/metrics-mlflow-2.png)](https://postimg.cc/PL5ywDyq)
