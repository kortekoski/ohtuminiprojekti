#!/usr/bin/env bash
set -e

main () {
   setup_db
   start_app
   start_tests
   teardown
}

setup_db () {
    echo "starting testing db..."
    docker compose up -d db
    echo "waiting for testing db to become available..."
    while [ "$(docker inspect -f '{{.State.Health.Status}}' $(docker compose ps -q db))" != "healthy" ]; do
          sleep 1
    done
}

start_app() {
    echo "starting app..."
    poetry run python src/index.py &
    MAIN_PID=$!
    echo "waiting for app to become available..."
    while [[ "$(curl -s -o /dev/null -w ''%{http_code}'' localhost:5001)" != "200"  ]]; do
        sleep 1
    done
}

start_tests() {
    echo "starting unittests..."
    poetry run coverage run -m pytest
    echo "starting robot tests..."
    poetry run robot src
}

teardown() {
    echo "tearing everything down..."
    # Try sending SIGTERM first
    kill -SIGTERM $MAIN_PID
    # Kill the process unceremoniously if SIGTERM fails
    # for whatever reason.
    if [[ $? != 0 ]]; then
       kill -9 $MAIN_PID
    fi
    docker compose down
}

main
