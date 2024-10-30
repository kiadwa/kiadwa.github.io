#!/bin/bash

source /home/ubuntu/Lab-01-Group-06/Backend/.venv/bin/activate
uwsgi --ini /home/ubuntu/Lab-01-Group-06/Backend/uwsgi.ini --plugin /usr/lib/uwsgi/plugins/python3_plugin.so
