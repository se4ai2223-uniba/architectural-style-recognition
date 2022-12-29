import os
from locust import HttpUser, task
external =  os.path.join("data","external")
class ClassifyLoadTest(HttpUser):
    
    @task
    def classify(self):
        test_file = os.path.join(external,"test_file", "pyramid.jpg")
        self.client.post('classify_image/',
                        files={'imgfile': open(test_file, 'rb')})