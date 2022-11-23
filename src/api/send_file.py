import requests
import os


#metodo che invia un file all'endpoint adibito
def post_file(endpoint, filepath):
        print(filepath)
        file = {'imgfile': open(filepath, 'rb')}
        resp = requests.post(url=endpoint, files=file)
        print(resp.json())

post_file('http://127.0.0.1:8000/predict/', os.path.join( "src", "api", "tests", "test_file", "pyramid.jpg"))