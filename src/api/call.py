import json
import requests
response = requests.post("http://127.0.0.1:8000/eval_class/?id_img=1&new_class=pupu")
print (json.loads(response.text))