#!/bin/bash

export APP_HOME=/usr/local/ls-host-server
cd ${APP_HOME}
source ./.env/bin/activate
python3 ./pcat-manager-web-main.py
