#!/bin/sh
echo "Started Shell-Script"
if [ "$CRON_TYPE" = "daily" ]; then
  echo "Initiated as daily"
  crontab crontab_daily_calls
else
  echo "Initiated not as daily"
  crontab crontab_default_5
fi

crond -f