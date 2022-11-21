import json
import os
file_name = os.path.join('..', '..', 'data','json','id.json')
def read_id():    
    f = open(file_name)
    data = json.load(f)
    i = data['next_id']
    f.close()
    return (i)    

def increase_id():
    # Opening JSON file
    f = open(file_name)
    data = json.load(f)
    f.close()
    data['next_id'] = data['next_id']+1
    f = open(file_name,'w')
    json.dump( data , f)
    f.close()