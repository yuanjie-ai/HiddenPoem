#!/usr/bin/env bash

gunicorn main:app -b 0.0.0.0:9955  -w 1 -k uvicorn.workers.UvicornH11Worker