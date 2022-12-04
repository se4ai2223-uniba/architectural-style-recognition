FROM python:3.9

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY requirements.txt /home/archinet/requirements.txt
RUN pip install --no-cache-dir -r /home/archinet/requirements.txt


COPY src/models /home/archinet/src/models
COPY src/data /home/archinet/src/data
COPY src/api /home/archinet/src/api
COPY models/saved-model-optimal /home/archinet/models/saved-model-optimal
COPY data /home/archinet/data
COPY params.yaml /home/archinet/params.yaml

WORKDIR /home/archinet
CMD ["uvicorn", "src.api.server:app", "--reload", "--host", "0.0.0.0", "--port", "81"]

#docker build -t fastapi_image .
#docker run -p 80:80 fastapi_image
#docker run -d -p 81:81   --name fastapi_container   --mount source=fastapi_volume,target=/data fastapi_image:latest