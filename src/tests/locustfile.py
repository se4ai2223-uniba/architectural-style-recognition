import os
import random
import glob
from locust import HttpUser, task

external = os.path.join("data", "external")
test_dir = os.path.join(external, "test_file")
dir_dict = glob.glob(os.path.join(test_dir, "*"))
upper_bound = len(dir_dict) - 1


class ClassifyLoadTest(HttpUser):
    @task
    def classify(self):
        test_file = dir_dict[random.randint(0, upper_bound)]
        self.client.post("/classify_image/", files={"imgfile": open(test_file, "rb")})
