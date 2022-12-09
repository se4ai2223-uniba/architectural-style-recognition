# Important notes

-   The script cronjob.py must be in the same directory of the Dockerfile (the root in this case).
-   The script called cronjob.py will be periodically called by the cron daemon on the host machine in order to move the images, correctly labeled by the experts, inside the raw dataset.
-   The script also removes the rows corresponding to the moved images from the dataset.csv and predictions.csv.
-   The script logs the errors into the file /home/archinet/log-cron.txt


## Image Names

The script collects the ids of the images from their name by searching to the first underscore, which 'stops' the numbers of the id. If the naming convention of the images changes, it's needed to change the function clean_data accordingly.

## Folders names

It is needed to lower all the names of the raw dataset folder in order to move the images into them. 
This because the class names saved into the dictionary.csv files are all lowered.

# To-fix

The numeric range of the label was changed. This led to wrong behaviour in this script since the old label values are still present in the .csv files. 
Thw wrong beahviour is that the images are moved to wrong folders due to the conversion used in the dictionary. 

