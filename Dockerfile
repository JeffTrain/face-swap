# syntax=docker/dockerfile:1

FROM python:latest

RUN apt update && apt install -y cmake g++ make ffmpeg libsm6 libxext6

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "--app", "hello", "run", "--host", "0.0.0.0"]