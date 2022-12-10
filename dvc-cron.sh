/usr/local/bin/python3 /home/archinet/cronjob.py >> /home/archinet/log-cron.txt  2>&1
dvc commit /home/archinet/data/raw/arcDataset -f
dvc push /home/archinet/data/raw/arcDataset
git add  /home/archinet/data/raw/arcDataset.dvc
git commit -m 'Update raw dataset'
git push -f