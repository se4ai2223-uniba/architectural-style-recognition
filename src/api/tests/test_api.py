import pytest
import os
import requests
import os
import csv
from src.api.utils import *
from http import HTTPStatus
import shutil

predict_endpoint = 'http://127.0.0.1:8000/predict/'
upload_endpoint = 'http://127.0.0.1:8000/uploadfile/'
eval_class_endpoint = 'http://127.0.0.1:8000/eval_class/'

def delete_last_row_csv(filename):
    csv_file = os.path.join("..","..","..","data","external", filename)
    f = open(csv_file, "r+")
    lines = f.readlines()
    lines.pop()
    f = open(csv_file, "w+")
    f.writelines(lines)

def remove_file(filename):
     os.remove(os.path.join("..","..","..","data","external","images", filename))

def test_predict_ok():
    test_file = os.path.join("test_file", "pyramid.jpg")
    resp = requests.post(url=predict_endpoint, files={'imgfile': open(test_file, 'rb')})
    id=resp.json()['id']
    filename=id+'_'+resp.json()['filename']
    remove_file(filename)
    delete_last_row_csv('predictions.csv')
    assert resp.status_code == HTTPStatus.OK

def test_predict_ko():
    test_file = os.path.join("test_file", "non_img.txt")
    resp = requests.post(url=predict_endpoint, files={'imgfile': open(test_file, 'rb')})
    assert resp.status_code == HTTPStatus.NOT_ACCEPTABLE

def test_upload_ok():
    test_file = os.path.join("test_file", "hadid.jpg")
    myobj = {'label': '1'}
    resp = requests.post(url=upload_endpoint, files={'imgfile': open(test_file, 'rb')}, params = myobj)
    id=resp.json()['id']
    filename=id+'_'+resp.json()['filename']
    remove_file(filename)
    delete_last_row_csv('dataset.csv')
    assert resp.status_code == HTTPStatus.OK

def test_upload_ko_image():
    test_file = os.path.join("test_file", "non_img.txt")
    myobj = {'label': '1'}
    resp = requests.post(url=upload_endpoint, files={'imgfile': open(test_file, 'rb')}, params = myobj)
    assert resp.status_code == HTTPStatus.NOT_ACCEPTABLE

def test_uploadt_ko_id():
    test_file = os.path.join(  "test_file", "hadid.jpg")
    myobj = {'label': '10'}
    resp = requests.post(url=upload_endpoint, files={'imgfile': open(test_file, 'rb')}, params = myobj)
    assert resp.status_code == HTTPStatus.NOT_ACCEPTABLE

def test_eval_class_ok():
    test_file = os.path.join("test_file", "pyramid.jpg")
    resp = requests.post(url=predict_endpoint, files={'imgfile': open(test_file, 'rb')})
    id=resp.json()['id']
    filename=id+'_'+resp.json()['filename']

    myobj = {'id_img': id, 'new_class':'2'}
    resp_eval = requests.put(url=eval_class_endpoint, files={'imgfile': open(test_file, 'rb')}, params = myobj)
    remove_file(filename)
    delete_last_row_csv('predictions.csv')
    delete_last_row_csv('dataset.csv')
    assert resp_eval.status_code == HTTPStatus.OK

def test_eval_class_ko_not_found():
    test_file = os.path.join("test_file", "pyramid.jpg")
    resp = requests.post(url=predict_endpoint, files={'imgfile': open(test_file, 'rb')})
    id=resp.json()['id']
    filename=id+'_'+resp.json()['filename']

    myobj = {'id_img': str(int(id)+1), 'new_class':'2'}
    resp_eval = requests.put(url=eval_class_endpoint, files={'imgfile': open(test_file, 'rb')}, params = myobj)
    remove_file(filename)
    delete_last_row_csv('predictions.csv')
    assert resp_eval.status_code == HTTPStatus.NOT_FOUND

def test_eval_class_ko_double():
    test_file = os.path.join("test_file", "pyramid.jpg")
    resp = requests.post(url=predict_endpoint, files={'imgfile': open(test_file, 'rb')})
    id=resp.json()['id']
    filename=id+'_'+resp.json()['filename']

    myobj = {'id_img': id, 'new_class':'2'}
    resp_eval = requests.put(url=eval_class_endpoint, files={'imgfile': open(test_file, 'rb')}, params = myobj)
    myobj = {'id_img': id, 'new_class':'3'}
    resp_eval_double = requests.put(url=eval_class_endpoint, files={'imgfile': open(test_file, 'rb')}, params = myobj)

    remove_file(filename)
    delete_last_row_csv('predictions.csv')
    delete_last_row_csv('dataset.csv')
    assert resp_eval_double.status_code == HTTPStatus.NOT_ACCEPTABLE