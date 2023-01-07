# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

RUN apt update && apt install -y cmake g++ make ffmpeg libsm6 libxext6 wget
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "--app", "hello", "run", "--host", "0.0.0.0"]