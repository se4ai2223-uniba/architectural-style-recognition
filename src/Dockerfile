FROM python:3.9-slim

RUN  python3 -m pip install --upgrade pip 
COPY requirements.txt /home/archinet/requirements.txt
RUN python3 -m pip install --no-cache-dir -r /home/archinet/requirements.txt

COPY frontend /home/archinet/src/frontend

WORKDIR /home/archinet
EXPOSE 82
CMD uvicorn src.frontend.static.frontend:app --reload --host 0.0.0.0 --port 82

#docker build src -t frontend_image
#docker run -d -p 9200:82 --name frontend_container frontend_image