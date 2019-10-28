#!/bin/bash

sudo heroku container:push --app gentle-basin-68908 web
sudo heroku container:release --app gentle-basin-68908 web
