'''This module provides a set of tests for the API endpoints'''
import os
from http import HTTPStatus
from fastapi.testclient import TestClient
from src.api import server

PREDICT_ENDPOINT = 'http://127.0.0.1:80/predict/'
UPLOAD_ENDPOINT = 'http://127.0.0.1:80/uploadfile/'
EVAL_CLASS_ENDPOINT = 'http://127.0.0.1:80/eval_class/'

external =  os.path.join("data","external")

client = TestClient(server.app)

def delete_last_row_csv(filename):
    '''Utility function that remove the lasdt row of a csv file'''
    csv_file = os.path.join(external, filename)
    file = open(csv_file, "r+")
    lines = file.readlines()
    lines.pop()
    file = open(csv_file, "w+")
    file.writelines(lines)

def remove_file(filename):
    '''utility function that remove a file'''
    os.remove(os.path.join(external,"images", filename))

def test_predict_ok():
    '''Test that the predict image function works well for a valid image'''
    test_file = os.path.join(external,"test_file", "pyramid.jpg")

    resp = client.post(url=PREDICT_ENDPOINT,
                        files={'imgfile': open(test_file, 'rb')})

    id_img=resp.json()['id']
    label=resp.json()['label']
    original_filename = resp.json()['filename']
    filename=id_img+'_'+original_filename
    remove_file(filename)
    delete_last_row_csv('predictions.csv')
    assert resp.status_code == HTTPStatus.OK
    assert resp.json() == {"filename": original_filename, "id": id_img, "label": label}

def test_predict_ko():
    '''Test that the ko is given when a file that is not an image is given in input'''
    test_file = os.path.join(external,"test_file", "non_img.txt")

    resp = client.post(url=PREDICT_ENDPOINT,
                        files={'imgfile': open(test_file, 'rb')})

    assert resp.status_code == HTTPStatus.NOT_ACCEPTABLE
    assert resp.json() == {'detail': 'Image upload error, the file provided is not an image.'}

def test_upload_ok():
    '''Test that the upload image function works well for a valid image and a valid label'''
    test_file = os.path.join(external,"test_file", "hadid.jpg")
    myobj = {'label': '4'}

    resp = client.post(url=UPLOAD_ENDPOINT,
                        files={'imgfile': open(test_file, 'rb')},
                        params = myobj)

    id_img=resp.json()['id']
    original_filename = resp.json()['filename']
    filename=id_img+'_'+original_filename
    remove_file(filename)
    delete_last_row_csv('dataset.csv')
    assert resp.status_code == HTTPStatus.OK
    assert resp.json() == {"filename": original_filename, "id": id_img, "label": 4}

def test_upload_ko_image():
    '''Test that the ko is given when a file that is not an image is given in input'''
    test_file = os.path.join(external,"test_file", "non_img.txt")
    myobj = {'label': '4'}

    resp = client.post(url=UPLOAD_ENDPOINT,
                        files={'imgfile': open(test_file, 'rb')},
                        params = myobj)

    assert resp.status_code == HTTPStatus.NOT_ACCEPTABLE
    assert resp.json()== {'detail': 'Image upload error, the file provided is not an image.'}

def test_upload_ko_id():
    '''Test that the ko is given when a non valid label is provided'''
    test_file = os.path.join( external,"test_file", "hadid.jpg")
    myobj = {'label': '10'}

    resp = client.post(url=UPLOAD_ENDPOINT,
                        files={'imgfile': open(test_file, 'rb')},
                        params = myobj)

    assert resp.json()== {'detail': 'Id label error, the label must be a value between 0 and 9.'}

def test_eval_class_ok():
    '''Test that no error is given when a single feedback is provided for an existent image'''
    test_file = os.path.join(external,"test_file", "pyramid.jpg")

    resp = client.post(url=PREDICT_ENDPOINT,
                        files={'imgfile': open(test_file, 'rb')})

    id_img=resp.json()['id']
    filename=id_img+'_'+resp.json()['filename']
    myobj = {'id_img': id_img, 'new_class':'2'}

    resp_eval = client.put(url=EVAL_CLASS_ENDPOINT,
                            params = myobj)

    remove_file(filename)
    delete_last_row_csv('predictions.csv')
    delete_last_row_csv('dataset.csv')
    assert resp_eval.status_code == HTTPStatus.OK
    assert resp_eval.json() =={"result": "ok, new class saved"}

def test_eval_class_ko_not_found():
    '''Test that the ko is given when a feedback is provided for a non existent image'''
    test_file = os.path.join(external,"test_file", "pyramid.jpg")

    resp = client.post(url=PREDICT_ENDPOINT,
                        files={'imgfile': open(test_file, 'rb')})

    id_img=resp.json()['id']
    filename=id_img+'_'+resp.json()['filename']

    myobj = {'id_img': str(int(id_img)+1), 'new_class':'2'}

    resp_eval = client.put(url=EVAL_CLASS_ENDPOINT,
                            params = myobj)

    remove_file(filename)
    delete_last_row_csv('predictions.csv')
    assert resp_eval.status_code == HTTPStatus.NOT_FOUND
    assert resp_eval.json() == {'detail': 'There is no classified image with that id.'}

def test_eval_class_ko_double():
    '''Test that the ko is given when a multiple feedback is provided for the same image'''
    test_file = os.path.join(external,"test_file", "pyramid.jpg")

    resp = client.post(url=PREDICT_ENDPOINT,
                        files={'imgfile': open(test_file, 'rb')})

    id_img=resp.json()['id']
    filename=id_img+'_'+resp.json()['filename']

    myobj = {'id_img': id_img, 'new_class':'2'}

    client.put(url=EVAL_CLASS_ENDPOINT,
                params = myobj)

    myobj = {'id_img': id_img, 'new_class':'3'}

    resp_eval_double = client.put(url=EVAL_CLASS_ENDPOINT,
                                    params = myobj)

    remove_file(filename)
    delete_last_row_csv('predictions.csv')
    delete_last_row_csv('dataset.csv')
    assert resp_eval_double.status_code == HTTPStatus.NOT_ACCEPTABLE
    assert resp_eval_double.json() == {'detail': 'There is already a class specified for that that image id.'}
