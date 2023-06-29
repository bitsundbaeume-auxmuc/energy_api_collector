FROM python:3.11-alpine

WORKDIR /code

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY crontab_default_5 crontab_default_5
COPY crontab_daily_calls crontab_daily_calls
COPY cron_job_handling.sh cron_job_handling.sh

COPY app /code/app

ENTRYPOINT ["./cron_job_handling.sh"]