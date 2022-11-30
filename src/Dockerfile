FROM python:3.9

WORKDIR /src

COPY req.txt /tmp/req.txt

RUN pip install --no-cache-dir -r /tmp/req.txt

COPY ./prova_docker /src/prova_docker

CMD ["uvicorn", "prova_docker.main:app", "--host", "0.0.0.0", "--port", "5000"]