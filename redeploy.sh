docker pull roblor/se4ai:latest
docker stop fastapi_container
docker container prune -f 
docker image prune -f
docker run -d -p 9100:81   --name fastapi_container   --mount source=fastapi_volume,target=/home/archinet/data roblor/se4ai:latest
