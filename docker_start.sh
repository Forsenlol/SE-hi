#!/bin/bash

sudo heroku container:push --app $HEROKU_APP_NAME web
sudo heroku container:release --app $HEROKU_APP_NAME web
