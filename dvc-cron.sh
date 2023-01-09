#!/bin/bash
curl -X GET https://betteruptime.com/api/v1/heartbeat/oJMDi3hU2YV9A1u1xHencsqh
/usr/local/bin/python3 /home/archinet/cronjob.py >> /home/archinet/pylog-cron.txt  2>&1
cd /home/archinet/
/usr/local/bin/dvc add /home/archinet/data/raw/arcDataset
/usr/local/bin/dvc commit /home/archinet/data/raw/arcDataset -f
/usr/local/bin/dvc push /home/archinet/data/raw/arcDataset
git add  /home/archinet/data/raw/arcDataset.dvc
git commit -m 'Cron job: update of raw dataset'
git push 

