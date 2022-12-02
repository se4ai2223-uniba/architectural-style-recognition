FROM python:3.9

WORKDIR /

COPY requirements.txt /src/requirements.txt
COPY src/models /src/models
COPY src/data /src/data
COPY src/api /src/api
COPY models/saved-model-optimal /src/models/saved-model-optimal
COPY data data
COPY params.yaml /src/params.yaml

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install --no-cache-dir -r /src/requirements.txt

CMD ["uvicorn", "src.api.server:app", "--host", "0.0.0.0", "--port", "80"]

#docker build -t fastapi_image .
#docker run -p 80:80 fastapi_image