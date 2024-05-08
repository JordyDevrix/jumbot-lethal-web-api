FROM ubuntu:latest
LABEL authors="2109j"

ADD . .

EXPOSE 5100

RUN pip install discord discord.py Quart==0.19.5