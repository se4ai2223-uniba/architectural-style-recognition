FROM python:3.9

COPY requirements.txt /home/archinet/requirements.txt
RUN pip install --no-cache-dir -r /home/archinet/requirements.txt

RUN apt-get update
RUN apt-get -y install ffmpeg libsm6 libxext6 
RUN apt-get -y install cron
RUN apt-get -y install vim


COPY src/models /home/archinet/src/models
COPY src/data /home/archinet/src/data
COPY src/api /home/archinet/src/api
COPY models/saved-model-optimal /home/archinet/models/saved-model-optimal
COPY params.yaml /home/archinet/params.yaml
COPY data /home/archinet/data

COPY dvc.yaml /home/archinet/dvc.yaml
COPY dvc.lock /home/archinet/dvc.lock
COPY .dvc /home/archinet/.dvc
COPY .git /home/archinet/.git
COPY .gitignore /home/archinet/.gitignore


# Copy dvc-cron file to the cron.d directory
COPY dvc-cron /etc/cron.d/dvc-cron
# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/dvc-cron
# Apply cron job
RUN crontab /etc/cron.d/dvc-cron

WORKDIR /home/archinet
EXPOSE 81
CMD /usr/sbin/cron && uvicorn src.api.server:app --reload --host 0.0.0.0 --port 81



#docker build . -t roblor/se4ai 
#docker run -d -p 9100:81   --name fastapi_container   --mount source=fastapi_volume,target=/home/archinet/data roblor/se4ai:latest