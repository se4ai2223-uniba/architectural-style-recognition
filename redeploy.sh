#!/bin/bash
docker pull roblor/se4ai:latest
docker compose down
docker container prune -f 
docker image prune -f
docker compose build
docker compose up