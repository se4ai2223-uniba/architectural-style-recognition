
# Quality Assurance in ML 

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Testing Data](#tesingdata)
- [Testing Code](#tesingdata)
- [Testing Model](#tesingdata)
- [Putting All Toghether](#tesingdata)


## Testing Data
In a ML model data are the most critical aspect, as the motto says "trash in - trash out" so we need to carefully check if data are coherent with a set of predifined quality check and avoid that strange values could spoil the training phase and the overall model's quality.

Especially in dataset that grow over time, for example colllecting users data, this step is crucial since there are chance that users could send non realible data.

## Great Expectation
A tool that can help us to do this kind of tests is Great Expectation.
It offers a set of functionality that helps developers to build up reliable tests on datasets.
Great Expectation is oriented to tabular data and not images like in our project, but this has not been a problem, we have extracted a set of informations from our dataset and saved them into a .csv file generated before applyng the GE test suite.
The informations are the followings:
<ul>
    <li>File Name </li>
    <li>File Type </li>
    <li>Label </li>
    <li>Colors (Y/N)</li>
    <li>Height </li>
    <li>Width </li>
    <li>Variance of the Laplacian Filter </li>
</ul>

The GE suite has been created importing the GE library and running the following commands:

    great_expectations init
    great_expectations datasource new
    great_expectations suite new
    great_expectations checkpoint new img_feature_checkpoint
    
that, in order: create the whole infrastructure, link GE to the file that we want to check, create the test suite and create the checkpoint that is the mechanism that allows to run the tests.

The test suite is a json file presents in great_expectations\expectations\img_features_suite.json were it's possible to express the kind of test, the checked column and the accetable values for that column, for example:

    {
      "expectation_type": "expect_column_values_to_be_between",
      "kwargs": {
        "column": "height",
        "include_unexpected_rows": true,
        "min_value": 50,
        "result_format": "COMPLETE",
        "strict_min": true
      },
      "meta": {}
    },

This test checks that the column heigh has value greater than 50, this in order to avoid to train our model on really small images that have too less details and becaime noisy when scaled up.

The whole test suite include the followings tests:
<ul>
    <li>Check on the label name: we want to avoid label that are not coherent with our pourposes</li>
    <li>Check on the color type: we want to allow or deny the possibility to add greyscale images</li>
    <li>Check on the variance of the laplacian filter greater than 0: if the lapliacianc variance is 0 the image is monochromatic and then non informative, we want to block this kind of data</li>
    <li>Checks on the heigh greater than 50: in order to avoid pictures that are too small</li>
    <li>Checks on the width greater than 50: in order to avoid pictures that are too small</li>
</ul>

All the execution are stored into:

    great_expectations\uncommitted\validations\img_features_suite

and is possbile to see the results throught a GUI using the html page sotred in:

    great_expectations/uncommitted/data_docs/local_site/index.html

##Testing Code
In order to verify that the code perform its task in a correct way we need a mechanism that run the code in a close context and make assertion about the correctness of the results.
This mechanisms are the Unit Test anche the Integration Test, the first type check the correctness of a function or a method, the second check the correctness of a whole sequence of modules.
In our project Pytest has been used in order to implement this kind of test and we have checked the correctness of the following modules:

<ul Dataset Preprocessing Functionalities>
    <li>Dataset class selection</li>
    <li>Dataset Splitting</li>
    <li>Dataset Augmentation</li>
</ul>
