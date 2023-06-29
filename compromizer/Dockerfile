FROM python:3.11-alpine

WORKDIR /code

RUN apk add build-base
RUN apk add linux-headers

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY crontab crontab

COPY app /code/app

WORKDIR /code

RUN crontab crontab

CMD ["crond", "-f"]