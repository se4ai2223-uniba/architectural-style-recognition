
# 🧰 Quality Assurance in ML 

## Table of Contents

- [Testing Data](#testing-data)
  - [Great Expectations](#great-expectations)
- [Testing Code](#testing-code)
- [Testing Model](#testing-model)


## ⚙️ Testing Data
In a ML model data are the most critical aspect, as the motto says "trash in - trash out" so we need to carefully check if data are coherent with a set of predefined quality check and avoid that strange values could spoil the training phase and the overall model's quality.

Especially in dataset that grow over time, for example collecting users data, this step is crucial since there are chance that users could send non reliable data.

### <b> Great Expectations </b> <img src='..\great_expectations\logo.png' style='width:20pt; vertical-align:middle'></img>
A tool that can help us to do this kind of tests is Great Expectations.
It offers a set of functionality that helps developers to build up reliable tests on datasets.
Great Expectations is oriented to tabular data and not images like in our project, but this has not been a problem, we have extracted a set of informations from our dataset and saved them into a .csv file generated before applyng the GE test suite.
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

    great_expectations\results\validations

and is possbile to see the results throught a GUI using the html page sotred in:

    great_expectations\results\data_docs\local_site\index.html

## ⚙️ Testing Code

In order to verify that the code perform its task in a correct way we need a mechanism that run the code in a close context and make assertion about the correctness of the results.
This mechanisms are the <b>Unit Test</b> and the <b>Integration Test</b>, the first type check the correctness of a function or a method, the second check the correctness of a whole sequence of modules.
In our project Pytest has been used in order to implement this kind of test and we have checked the correctness of the following modules:

<b>Dataset Preprocessing Functionalities Tests</b>

📁- tests\test_dataset_code.py

<table>
  <tr>
    <th>Test Subject</th>
    <th>Test method</th>
    <th>Test type</th>
    <th>Result</th>
  </tr>
  <tr>
    <td>Dataset class selection</td>
    <td>test_selectClasses()</td>
    <td>Unit Test</td>
    <td> ✔️ </td>
  </tr>
  <tr>
    <td>Dataset Splitting</td>
    <td>test_splitting()</td>
    <td>Unit Test</td>
    <td> ✔️ </td>
  </tr>
  <tr>
    <td>Dataset Augmentation</td>
    <td>test_data_augmentation()</td>
    <td>Unit Test</td>
    <td> ✔️ </td>
  </tr>

</table>


All these tests has been performed on a sample of data just enough to verify that the modules produces the expected results.
In order to easily create and manage this sample we have used the Pytest decorator fixture with autouse:

    @pytest.fixture(autouse=True)
    def prepareTestData():

        if os.path.exists(src_path):
            shutil.rmtree(src_path)

        shutil.copytree(orig_path, src_path)
        yield src_path
        shutil.rmtree(src_path)
        if os.path.exists(dst_path):
            ut.remove_content(dst_path)

that allow to every test to run the file system utilities needed to perform each test.

Then, also the code of the model definition has been tested:

<b>ML Model Definition Tests</b>

📁 - tests\test_model.py

<table>
  <tr>
    <th>Test Subject</th>
    <th>Test method</th>
    <th>Test type</th>
    <th>Result</th>
  </tr>
  <tr>
    <td>YAML Params</td>
    <td>test_params()</td>
    <td>Unit Test</td>
    <td> ✔️ </td>
  </tr>
  <tr>
    <td>Model input & output</td>
    <td>test_buildModel()</td>
    <td>Unit Test</td>
    <td> ✔️ </td>
  </tr>
  <tr>
    <td>Training Phase</td>
    <td>test_trainModel()</td>
    <td>Integration Test</td>
    <td> ✔️ </td>
  </tr>
</table>

In particular the second test checks that the builded model has the expected layer dimensions, the third instead, since has the aim of test the actual correctness of the whole trainig phase, needs to call all the steps of our pipeline and for this reason has the role of an integration test.

## ⚙️ Testing Model

In a ML workflow is necessary to verify that every version of a model satisfy a set of condition on its performances. These kind of tests are called <b>System Test</b> and are performed on the output model of our ML pipeline.
In our project also these kind of test has been implemented using pytest tests and are the followings:
<b>ML Model Evaluation Tests</b>

📁 - tests\test_performances.py

<table>
  <tr>
    <th>Test Subject</th>
    <th>Test method</th>
    <th>Test type</th>
    <th>Result</th>
  </tr>
  <tr>
    <td>Check on metrics</td>
    <td>test_modelPerformances()</td>
    <td>System Test</td>
    <td> ✔️ </td>
  </tr>
  <tr>
    <td>Check directionality on image</td>
    <td>test_minimum_functionality()</td>
    <td>Minimum Functionality Test</td>
    <td> ❌ </td>
  </tr>
  <tr>
    <td>Check invariance on image</td>
    <td>test_invariance()</td>
    <td>System Test</td>
    <td> ❌ </td>
  </tr>
</table>

For the first test we have checked that the accuracy and the f1-scorse was greater than a predifined treshold, for the second test we have checked that differently labeled inputs was classified in different way, for the third one we have checked that slightly different inputs reffering to the same class was classified in the same way.