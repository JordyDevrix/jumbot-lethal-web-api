FROM python:3.10
LABEL authors="2109j"

ADD . .

EXPOSE 5100

RUN pip install discord discord.py Quart==0.19.5

CMD python app.py