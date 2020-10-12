#!/usr/bin/env bash

set -ex

EXEC_CMD ='docker-compose run backend'

docker-compose up --build -d

${EXEC_CMD} python manage.py migrate
${EXEC_CMD} python manage.py createsuperuse --no-input
${EXEC_CMD} python manage.py test