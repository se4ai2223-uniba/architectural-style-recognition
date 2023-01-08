# Important notes

-   The shell script dvc-cron.sh  must be in the same directory of the Dockerfile. This script will execute cronjob.py and the commands to track the data through dvc and git.
-   The python script cronjob.py must be in the same directory of the Dockerfile.
-   The script called cronjob.py will be periodically called by the cron daemon on the host machine in order to move the images, correctly labeled by the experts, inside the raw dataset.
-   The script also removes the rows corresponding to the moved images from the dataset.csv and predictions.csv.
-   The script logs the errors into the file /home/archinet/log-cron.txt


## Image Names

The script collects the ids of the images from their name by searching to the first underscore, which 'stops' the numbers of the id. If the naming convention of the images changes, it's needed to change the function clean_data accordingly.

## Folders names

It is needed to lower all the names of the raw dataset folder in order to move the images into them. 
This because the class names saved into the dictionary.csv files are all lowered.
