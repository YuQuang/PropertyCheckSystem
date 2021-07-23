#!/bin/bash
echo "Run Server"
daphne -b 0.0.0.0 -p 8000 Web.asgi:application &
uwsgi --ini pandian.ini