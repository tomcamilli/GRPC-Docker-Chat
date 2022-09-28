FROM ubuntu:bionic

RUN apt-get update
RUN apt-get install python3 python3-pip -y

COPY ./requirements.txt /requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 50051

WORKDIR /app
COPY . .
CMD ["/usr/bin/python3", "./src/chatter_server.py"]
