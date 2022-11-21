import json
import requests
response = requests.post("http://127.0.0.1:8000/eval_class/?id_img=14&new_class=3")
print (json.loads(response.text))