#!/usr/bin/env bash

set -ex

EXEC_CMD='docker-compose run backend'

docker-compose up --build -d

${EXEC_CMD} python manage.py migrate
${EXEC_CMD} python manage.py createsuperuser --username test1 --password 123321 --no-input
${EXEC_CMD} python manage.py test