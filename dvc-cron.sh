#!/bin/bash
/usr/local/bin/python3 /home/archinet/cronjob.py >> /home/archinet/pylog-cron.txt  2>&1
cd /home/archinet/
dvc commit /home/archinet/data/raw/arcDataset -f 
dvc push /home/archinet/data/raw/arcDataset
git add  /home/archinet/data/raw/arcDataset.dvc 
git commit -m 'Update raw dataset' 
git push 