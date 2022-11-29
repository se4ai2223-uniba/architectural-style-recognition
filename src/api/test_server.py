import os
import pytest
import requests
import os
from src.api.utils import *
from http import HTTPStatus
from fastapi.testclient import TestClient
import server

predict_endpoint = 'http://127.0.0.1:8000/predict/'
upload_endpoint = 'http://127.0.0.1:8000/uploadfile/'
eval_class_endpoint = 'http://127.0.0.1:8000/eval_class/'

external =  os.path.join("..","..","data","external")

client = TestClient(server.app)

def delete_last_row_csv(filename):
    csv_file = os.path.join(external, filename)
    f = open(csv_file, "r+")
    lines = f.readlines()
    lines.pop()
    f = open(csv_file, "w+")
    f.writelines(lines)

def remove_file(filename):
     os.remove(os.path.join(external,"images", filename))

def test_predict_ok():
    test_file = os.path.join(external,"test_file", "pyramid.jpg")
    resp = client.post(url=predict_endpoint, files={'imgfile': open(test_file, 'rb')})    
    id=resp.json()['id']
    label=resp.json()['label']
    original_filename = resp.json()['filename']
    filename=id+'_'+original_filename
    remove_file(filename)
    delete_last_row_csv('predictions.csv')
    assert resp.status_code == HTTPStatus.OK    
    assert resp.json() == {"filename": original_filename, "id": id, "label": label}

def test_predict_ko():
    test_file = os.path.join(external,"test_file", "non_img.txt")
    resp = client.post(url=predict_endpoint, files={'imgfile': open(test_file, 'rb')})
    assert resp.status_code == HTTPStatus.NOT_ACCEPTABLE
    assert resp.json() == {'detail': 'Image upload error, the file provided is not an image.'}

def test_upload_ok():
    test_file = os.path.join(external,"test_file", "hadid.jpg")
    myobj = {'label': '4'}
    resp = client.post(url=upload_endpoint, files={'imgfile': open(test_file, 'rb')}, params = myobj)
    id=resp.json()['id']
    original_filename = resp.json()['filename']
    filename=id+'_'+original_filename
    remove_file(filename)
    delete_last_row_csv('dataset.csv')
    assert resp.status_code == HTTPStatus.OK
    assert resp.json() == {"filename": original_filename, "id": id, "label": 4}

def test_upload_ko_image():
    test_file = os.path.join(external,"test_file", "non_img.txt")
    myobj = {'label': '4'}
    resp = client.post(url=upload_endpoint, files={'imgfile': open(test_file, 'rb')}, params = myobj)
    assert resp.status_code == HTTPStatus.NOT_ACCEPTABLE
    assert resp.json()== {'detail': 'Image upload error, the file provided is not an image.'}

def test_upload_ko_id():
    test_file = os.path.join( external,"test_file", "hadid.jpg")
    myobj = {'label': '10'}
    resp = client.post(url=upload_endpoint, files={'imgfile': open(test_file, 'rb')}, params = myobj)
    assert resp.json()== {'detail': 'Id label error, the label must be a value between 0 and 9.'}

def test_eval_class_ok():
    test_file = os.path.join(external,"test_file", "pyramid.jpg")
    resp = client.post(url=predict_endpoint, files={'imgfile': open(test_file, 'rb')})
    id=resp.json()['id']
    filename=id+'_'+resp.json()['filename']

    myobj = {'id_img': id, 'new_class':'2'}
    resp_eval = client.put(url=eval_class_endpoint, files={'imgfile': open(test_file, 'rb')}, params = myobj)
    remove_file(filename)
    delete_last_row_csv('predictions.csv')
    delete_last_row_csv('dataset.csv')
    assert resp_eval.status_code == HTTPStatus.OK
    assert resp_eval.json() =={"result": "ok, new class saved"}

def test_eval_class_ko_not_found():
    test_file = os.path.join(external,"test_file", "pyramid.jpg")
    resp = client.post(url=predict_endpoint, files={'imgfile': open(test_file, 'rb')})
    id=resp.json()['id']
    filename=id+'_'+resp.json()['filename']

    myobj = {'id_img': str(int(id)+1), 'new_class':'2'}
    resp_eval = client.put(url=eval_class_endpoint, files={'imgfile': open(test_file, 'rb')}, params = myobj)
    remove_file(filename)
    delete_last_row_csv('predictions.csv')
    assert resp_eval.status_code == HTTPStatus.NOT_FOUND
    assert resp_eval.json() == {'detail': 'There is no classified image with that id.'}


def test_eval_class_ko_double():
    test_file = os.path.join(external,"test_file", "pyramid.jpg")
    resp = client.post(url=predict_endpoint, files={'imgfile': open(test_file, 'rb')})
    id=resp.json()['id']
    filename=id+'_'+resp.json()['filename']

    myobj = {'id_img': id, 'new_class':'2'}
    resp_eval = client.put(url=eval_class_endpoint, files={'imgfile': open(test_file, 'rb')}, params = myobj)
    myobj = {'id_img': id, 'new_class':'3'}
    resp_eval_double = client.put(url=eval_class_endpoint, files={'imgfile': open(test_file, 'rb')}, params = myobj)

    remove_file(filename)
    delete_last_row_csv('predictions.csv')
    delete_last_row_csv('dataset.csv')
    assert resp_eval_double.status_code == HTTPStatus.NOT_ACCEPTABLE
    assert resp_eval_double.json() == {'detail': 'There is already a class specified for that that image id.'}