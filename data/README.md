---
annotations_creators:
- expert-generated
language:
- en
language_creators:
- expert-generated
- found
license:
- cc-by-nc-sa-4.0
multilinguality:
- monolingual
pretty_name: buildings_dataset
size_categories:
- 1K<n<10K
source_datasets:
- original
tags:
- image-classification
- computer-vision
- architectural-styles
- buildings
task_categories:
- image-classification
task_ids:
- multi-class-image-classification
---

# Dataset Card for Buildings Dataset

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks and Leaderboards](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits](#data-splits)
- [Dataset Creation](#dataset-creation)
  - [Curation Rationale](#curation-rationale)
  - [Source Data](#source-data)
  - [Annotations](#annotations)
  - [Personal and Sensitive Information](#personal-and-sensitive-information)
- [Additional Information](#additional-information)
  - [Dataset Curators](#dataset-curators)
  - [Licensing Information](#licensing-information)


## Dataset Description

- **Repository:** <a>https://www.kaggle.com/datasets/wwymak/architecture-dataset</a>
- **Paper:** <a>https://www.semanticscholar.org/paper/Architectural-Style-Classification-Using-Latent-Xu-Tao/bf6fd53680c5ec7b998c60bd75243d5b7cf7f93f?p2df</a>


### Dataset Summary

The dataset is a subset of the one used in the paper "Architectural Style Classification Using Multinomial Latent Logistic Regression", Zhe Xu et al.

The original dataset contains around 5000 images of buildings annotated according to 25 different classes (i.e. architectural styles). 

This number has been reduced to 2343 images and 10 classes in order to reduce time complexity in the training phase.

The 10 classes considered are:
1-Baroque
2-Byzantine
3-Art Deco
4-Art Nuveau
5-Egyptian
6-Ghotic
7-Greek
8-Art Nuveau
9-Romanesque
10-Russian

### Supported Tasks and Leaderboards

The model has been using for the task of classification of architectural styles, reaching an accuracy of around 84% on the test set.


### Languages

As the dataset is comprised of annotated images (in contrast to annotated documents), the language we refer to in only the one used in the annotations, which is exclusively English.

## Dataset Structure

### Data Instances

Each instance is constitued by a 224x224x3 image.

### Data Fields

As the dataset is comprised of images, there are no data fields.

### Data Splits

The training, validation and test proportion of the dataset are respectively 70%, 20% and 10%.

## Dataset Creation

### Curation Rationale

The dataset was created by the original authors of the cited paper to compensate for the lack of publicly available large-scale architectural style databases.

A subset of this dataset has been selected for the model in this project, in order to speed up training times.


### Source Data

#### Initial Data Collection and Normalization

According to the source paper, the dataset has been annotated by querying Wikimedia with the keyword "Architecture_by_style" and then downloading images from subcategories resulting from the query. Those images have then been manually filtered to exclude images of non-buildings, interior decorations, or part of a building, so that the remaining images only contained exterior facades of buildings. Furthermore, styles with too few images were discarded, resulting in a total of 25 styles.

Additional filtering was then applied to the dataset by the creators of our model, reducing the number of images to about a half and the number of classes to 10.

The two main types of normalization used are re-scaling normalization, which normalized each pixel value of an image to a number between 0 and 1, and mean STD normalization, used to normalize data to a uniform mean of 0 and a standard deviation of 1. These two normalizations have the overall purpose of speeding up the learning process of the neural network. 


#### Who are the source language producers?

The images were taken from Wikimedia, which stores them as freely available photos taken by a large number of individual users.

### Annotations

#### Annotation process

The annotations are those used in the citated paper, and are obtained according to their classification on Wikimedia, as previously mentioned.

#### Who are the annotators?

The annotators are the authors of the referred paper, namely: Zhe Xu, Dacheng Tao, Ya Zhang, Junjie Wu, and Ah Chung Tsoi

### Personal and Sensitive Information

The dataset, owing to its content, does not contain any kind of personal or sensitive information.

## Additional Information

### Dataset Curators

The curators are the authors of the referred paper, namely: Zhe Xu, Dacheng Tao, Ya Zhang, Junjie Wu, and Ah Chung Tsoi.

### Licensing Information

This dataset is distributed using a Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) license.