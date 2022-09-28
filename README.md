## Gocker Chat
by Thomas Camilli

A simple client-server chat program using python, GRPC, and docker. Allows for multiple clients to connect and communicate over a server using GRPC.
Two main python programs:
- src/chatter_client.py
- src/chatter_server.py

### Requirements:
* docker
* grpc
* python3

## Commands for starting the server in a docker container:
docker build -t gocker_chat_server .
docker run -p 50051:50051 -it gocker_chat_server

## Command for connecting to the server as a client, once the server is running:
python3 src/chatter_client.py
