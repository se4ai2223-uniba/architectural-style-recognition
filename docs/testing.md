
# Quality Assurance in ML 

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Testing Data](#tesingdata)
- [Testing Code](#tesingdata)
- [Testing Model](#tesingdata)
- [Putting All Toghether](#tesingdata)


## Testing Data
In a ML model data are the most critical aspect, as the motto says "trash in - trash out" so we need to carefully check if data are coherent with a set of predifined quality check and avoid that strange values could spoil the training phase and the overall model's quality.

Expceally in dataset that grow over time, for example colllecting users data, this step is crucial since there are chance that users could send non realible data.

## Great Expectation
A tool that can help us to do this kind of test is Great Expectation.
It offers a set of funcionality that helps developers to build up reliable test on datasets.
Great Expectation is oriente dto tabular data but this has not been a problem, we have extracted a set of information from our dataset and saved into a .csv file generated before applyng the GE test suite.
The information are the followings:
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

The test site is a json file presents in great_expectations\expectations\img_features_suite.json were it's possible to express the kind of test, the checked column anche the accetable values for that column, for example:

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

checks that the column heigh has value greater than 50, this in order to avoid to train our model on really small images that have too less details and becaime noisy when scaled up.
The whole test suite include the followings tests:
<ul>
    <li>Check on the label name: we want to avoid label that are not coherent with our pourposes</li>
    <li>Check on the color type: we want to allow or deny the possibility to add greyscale images</li>
    <li>Check on the variance of the laplacian filter greater than 0: if the lapliacianc variance is 0 the image is monochromatic and then non informative, we want to block this kind of data</li>
    <li>Checks on the heigh greater than 50: in order to avoid pictures that are too small</li>
    <li>Checks on the width greater than 50: in order to avoid pictures that are too small</li>
</ul>
