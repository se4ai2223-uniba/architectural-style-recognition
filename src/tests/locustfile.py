import os
import random
import glob
from locust import HttpUser, task, events
import argparse

#THIS SCRIPT NEEDS THE --folder parameter
# Run locust with images which belong to train data classes
# locust --web-host 0.0.0.0 -f src/tests/locustfile.py --folder 'test_file'

# Run locust with images which DON'T belong to train data classes
# locust --web-host 0.0.0.0 -f src/tests/locustfile.py --folder 'test_drift'




@events.init_command_line_parser.add_listener
def init_parser(parser):
    parser.add_argument(
        "--folder",
        metavar="path",
        required=True,
        help="the name of the folder at data/external, which contains the images that locust will send to the endpoint classify_image",
    )


class ClassifyLoadTest(HttpUser):
    @task
    def classify(self):
        folder = self.environment.parsed_options.folder
        test_dir = os.path.join("data", "external", folder)

        dict_imgs = glob.glob(os.path.join(test_dir, "*"))
        upper_bound = len(dict_imgs) - 1

        test_file = dict_imgs[random.randint(0, upper_bound)]
        self.client.post("/classify_image/", files={"imgfile": open(test_file, "rb")})