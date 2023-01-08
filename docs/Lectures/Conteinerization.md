# Conteinarization 📦

## Software Portability 

Portabiliy: Where, the software, can run.

- Heavy Solution: VM (Snapshot of the computer)
- Light Solution: Container

## Differences

- Virtual Machine need to communicate between two operating system managing App, Bins/Lib, Guest OS (for each app) (slower)

- With containers the operating system is just one and it handle, for each app, just the app and bins/libs. (faster)

the only case in which VM is better than container, is for test-security reasons.

## Some technologies that support Conteinerization

- Docker 🐋
- Kubernetes 🟥 (orchestrate services: which container start first, which later, handle errors in containers)


# Docker 🐋

Engine that automates the deployment of applications (services) into containers.

## Dockerfile
file that declare what must be included into a container

## Docker image

using command "docker build" that takes in input a "Dockerfile" give in output a "Docker image". A static file is produced and must be pushed in Docker Hub or **GitHub Packages** and downloaded with docker pull.

## Docker file example

- Base image (OS to emulate)
- Env variable 
- RUN command (execute any shell command)
- installing dependencies
- installing softwares (i.e. Python)
- open port
- start process

        #DOCKER FILE
        # Build a docker image
        FROM ubuntu:18.04 
        COPY . /app
        ADD # similar of copy
        ENV APP_HOME/myapp
        RUN mkdir $APP_HOME #shell commands
        # Execture some script
        EXPOSE port # example: the port of FAST API
        CMD python /app/app.py
        ENTRYPOINT #similar to CMD

The available FROM OS snapshots are available fromt docker hub.
Each commands, constitute layers that are cached.
***If a layer change than ALL changes below will be repeated!***

After wrote the docker file:

        docker build -t TAG_NAME

        docker image ls #list all images

        docker image rm # remove iamge

        docker pull TAG_IMAGE

        docker tag #rename an existing image

        docker push # push an image to a registry

        docker container run --name TAG_NAME -p 5000:80

        docker container stop TAG_NAME

        docker container kill TAG_NAME

## Managing Multiple Containers with Docker

docker-compose.yml is a pointer for multiple dockerfile that refer to different services.

        docker compose up #run all containers
        docker compose down #stop all


## Why contenairization is important to ML systems?

Same images and same model can produce bad results despite testing. This can be caused by operating system (example CV2 recognize pixels in different whay depending on OS).

 So we have to reproduce the best envirorment for our system replicating the OS. This is not the only case.



## More than 1 containers in one application? Kubernetes. 🟥

Kubernetes orchestrate the containers of a single system in order to handle them in case like: errors in one container, synchronize them, etc.