#!/bin/bash
source venv/bin/activate

while true; do
    flask deploy
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done

exec venv/bin/gunicorn -b :8000 --access-logfile - --error-logfile - "pystro:create_app()"
