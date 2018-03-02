FROM python:3.6-alpine
LABEL AUTHOR du2x <dudumonteiro@gmail.com>

ENV FLASK_APP pystro.py
ENV PYSTRO_SETTINGS api.config.DevelopmentConfig

RUN adduser -D pystro
USER pystro

WORKDIR /home/pystro

RUN python -m venv venv

COPY requirements requirements

RUN venv/bin/pip install -r requirements/docker.txt

COPY requirements.txt requirements.txt
RUN venv/bin/pip install -r requirements.txt

COPY api api
COPY migrations migrations

COPY pystro.py . 
COPY boot.sh .

# run-time configuration
EXPOSE 8000
ENTRYPOINT ["sh", "./boot.sh"]