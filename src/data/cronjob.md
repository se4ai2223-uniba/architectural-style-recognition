# Important notes

The script called cronjob.py wil be called by the cron daemon on the host machine in order to move the files correctly labeled by the experts inside the raw dataset.




## Image Names

The script collects the ids of the images from their name by searching to the first underscore, which 'stops' the numbers of the id. If the naming convention of the images changes, it's needed to change the function clean_data inside this script accordingly.

## Folders names

It is needed to lower all the names of the raw dataset folder in order to move the images into them. 
This because the class names saved into the dictionary.csv files are all lowered.
