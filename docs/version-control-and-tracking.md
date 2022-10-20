
# Version Control and Experiment Tracking

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Introduction](#introduction)
  - [Why Reproducibility?](#why-reproducibility)
  - [Data versioning, Pipeline and Experiment Tracking](#data-versioning-pipeline-and-experiment-tracking)
  - [Technologies: DVC, MLFlow, DagsHub](#technologies-dvc-mlflow-dagshub)
- [Code restructuring](#code-restructuring)
- [DVC](#dvc)
  - [Prepare-dataset](#prepare-dataset)
  - [Training](#training)
  - [Predict](#predict)
- [MLflow](#mlflow)
  - [Parameters](#parameters)
  - [Metrics](#metrics)
  - [Comparisons](#comparisons)
- [Additional Resources](#additional-resources)

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
In this project DVC is used for data versioning and for the implementation of the pipeline, then MLFlow is used for experiment tracking.
DagsHub has been adopted as storage for DVC and as hub for MLFlow having an unique place for our reproducibility tasks.




## Code Restructuring

In order to conform to the standard structure of a machine learning pipeline, we moved the original code from the original ipynb notebook to three different python files, corresponding to the three main steps of the pipeline.


[![pipeline-files.png](https://i.postimg.cc/pLPB6YkN/pipeline-files.png)](https://postimg.cc/zVPWLh9p)

Below we describe the general pipeline and its stages for our model.

## DVC

The dvc.yaml is divided into three stages, corresponding to the phases of our machine learning pipeline:
<ul>
    <li> Data preparation stage </li>
    <li> Training stage</li>
    <li> Evaluation stage</li>
</ul>

To each stage is associated:
<ul>
    <li> a python file, containing the code to be executed in that phase </li>
    <li> the dependencies required for the execution of the stage </li>
    <li> the output files generated at the end of the stage </li>
</ul>


### Prepare-dataset 

In this stage we prepare the data for further training and evaluation phases.
Below we illustrate the execution steps for this stage: 

<ul>
    <li> Select a set of classes from the original dataset
    <li> Extract train, validation and test set from the previuos selected calsses (further details can be found at <a ref=https://github.com/se4ai2223-uniba/architectural-style-recognition/blob/main/data/README.md> data card link </a>)</li>
</ul>

In order to add the stage to dvc.yaml file we execute the following command: 

    dvc run -n prepare-dataset \
    -d data/raw/arcDataset \
    -d src/data/make_dataset.py \
    -o data/processed/train \
    -o data/processed/val \
    -o data/processed/test \
    python src/data/make_dataset.py


### Training

In this stage we train the model, saving it inside the two files: 
<ul>
  <li> model.json: contains the model structure,
  <li> model.h5: contains the learned weights.
</ul>


Below we illustrate the execution steps for this stage: 

<ul>
    <li> Model building 
    <li> Preprocessing of images (further details can be found at <a ref=https://github.com/se4ai2223-uniba/architectural-style-recognition/blob/main/models/README.md#preprocessing> preprocessing </a>)
    <li> Model training
    <li> Saving of the model's parameters
</ul>

In order to add the stage to dvc.yaml file we execute the following command: 

    dvc run -n train \
    -d src/models/train_model.py \
    -d data/processed/train \
    -d data/processed/val \
    -o models/saved-model/model.json \
    -o models/saved-model/model.h5 \
    python src/models/train_model.py 

### Predict

In this stage we evaluate the model, making predictions on the test set, giving as output: 

<ul>
  <li> src/models/results.txt: contains the evaluation results for the accuracy. 
</ul>


In order to add the stage to dvc.yaml file we execute the following command: 

    dvc run -n predict \
    -d data/processed/test \
    -d models/saved-model/model.h5 \
    -d models/saved-model/model.json \
    -d src/models/predict_model.py \
    -o src/models/predictions.txt \
    python src/models/predict_model.py 

<br>
A graph representing the summary of our dvc pipeline is reported below:

<br>

![eb58fef3-5ecb-4fb3-bb94-794513ba69a0.jpg](https://i.postimg.cc/TwFLtbVC/Grafo.png)



## MLflow

To track parameters and metrics relevant to our ML model we have chosen MLflow. As a preliminary step, we have set as a tracking URI our DagsHub repository, so that we can visualize the results on that repository under the "Experiments" tab (or, alternatively, using the .mlflow URI).

Then, we have added the necessary code into the train_model.py and in the predict_model.py files, to track parameters and metrics. The code and the results on DagsHub are visible below.

### Parameters

[![params-code.png](https://i.postimg.cc/66GvKjQs/params-code.png)](https://postimg.cc/ThfwqcmQ)

[![params-mlflow.png](https://i.postimg.cc/FFjHG2RK/params-mlflow.png)](https://postimg.cc/hhtntZVF)


### Metrics

[![metrics-code.png](https://i.postimg.cc/HkKmT2xK/metrics-code.png)](https://postimg.cc/PCm9411z)

[![evaluation-metrics.png](https://i.postimg.cc/fbQz8xYF/evaluation-metrics.png)](https://postimg.cc/RWGxFJsQ)

### Comparison

One of the most important uses of MLflow is the comparison between different parameters based on their impact on the relevant metrics. Below we report a sample comparison between 3 different values of the learning rate, using validation accuracy as our metric. Four runs have been executed for each of the three values.

[![learning-rate-comparison.png](https://i.postimg.cc/52Nq6CXh/learning-rate-comparison.png)](https://postimg.cc/SJ3zPj7d)



## Additional Resources


  [DagsHub repo](https://dagshub.com/RobertoLorusso/architectural-style-recognition)
