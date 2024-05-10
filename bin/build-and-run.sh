#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PROJECT_ROOT=$DIR/..

cd $PROJECT_ROOT

ENV_FILE=.env
if test -f "$ENV_FILE"; then
    echo ".env file exists."
else
    ./bin/gen_env.sh
fi

docker-compose -f docker-compose.yml build --pull
docker-compose -f docker-compose.yml up -d --remove-orphans
