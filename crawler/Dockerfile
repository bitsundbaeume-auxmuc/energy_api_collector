FROM python:3.11-alpine

WORKDIR /code

COPY requirements.txt requirements.txt
COPY crontab crontab
RUN pip install -r requirements.txt

COPY app /code/app

WORKDIR /code

RUN crontab crontab

CMD ["crond", "-f"]