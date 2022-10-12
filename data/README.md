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
pretty_name: 
- buildings_dataset
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
- [Considerations for Using the Data](#considerations-for-using-the-data)
  - [Social Impact of Dataset](#social-impact-of-dataset)
  - [Discussion of Biases](#discussion-of-biases)
  - [Other Known Limitations](#other-known-limitations)
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
[![archi-style.png](https://i.postimg.cc/3xG3543f/archi-style.png)](https://postimg.cc/xX9wLdJL)

The ten classes are distributed as follow:

[![msg-876143422-143037.jpg](https://i.postimg.cc/sXgNnZTN/msg-876143422-143037.jpg)](https://postimg.cc/Ffwpz15y)
### Supported Tasks and Leaderboards

The model has been using for the task of classification of architectural styles, reaching an accuracy of around 84% on the test set.


### Languages

As the dataset is comprised of annotated images (in contrast to annotated documents), the language we refer to in only the one used is the annotations, which is exclusively English.

## Dataset Structure

### Data Instances

Each instance is constitued by images of different sizes.

### Data Fields

As the dataset is comprised of images, there are no data fields.

### Data Splits

The training and validation proportion of the dataset are respectively 70% and 30%.

The test set was build taking 30 images from the dataset and placing them in a proper folder, this was done in order to have a balanced test set and avoid biases in testing.

## Dataset Creation

### Curation Rationale

The dataset was created by the original authors of the cited paper to compensate for the lack of publicly available large-scale architectural style databases.

A subset of this dataset has been selected for the model in this project, in order to speed up training times.


### Source Data

#### Initial Data Collection and Normalization

According to the source paper, the dataset has been annotated by querying Wikimedia with the keyword "Architecture_by_style" and then downloading images from subcategories resulting from the query. Those images have then been manually filtered to exclude images of non-buildings, interior decorations, or part of a building, so that the remaining images only contained exterior facades of buildings. Furthermore, styles with too few images were discarded, resulting in a total of 25 styles.

Additional filtering was then applied to the dataset by the creators of our model, reducing the number of images to about a half and the number of classes to 10.


#### Who are the source language producers?

The images were taken from Wikimedia, which stores them as freely available photos taken by a large number of individual users.

### Annotations

#### Annotation process

The annotations are those used in the citated paper, and are obtained according to their classification on Wikimedia, as previously mentioned.

#### Who are the annotators?

The annotators are the authors of the referred paper, namely: Zhe Xu, Dacheng Tao, Ya Zhang, Junjie Wu, and Ah Chung Tsoi

### Personal and Sensitive Information

The dataset, owing to its content, does not contain any kind of personal or sensitive information.

## Considerations for Using the Data

### Social Impact of Dataset

The dataset has been developed to aid in the classification of architectural styles. While it does not purport to have be particularly impactful from a social standpoint, might still be considered useful to promote interest and stimulate curiosity in the study of different cultures.

### Discussion of Biases

Both the original dataset and the filtered one were imbalanced, meaning that some classes were more represented than others. Data augmentation has been used during the preprocessing phase to compensate for this problem.

### Other Known Limitations

As previously mention, the need for a faster model has been addressed with a reduction of the number of images and classes in the original model, respectively from around 5000 to 2343, and from 25 to 10.
## Additional Information

### Dataset Curators

The curators are the authors of the referred paper, namely: Zhe Xu, Dacheng Tao, Ya Zhang, Junjie Wu, and Ah Chung Tsoi.

### Licensing Information

This dataset is distributed using a Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) license.
