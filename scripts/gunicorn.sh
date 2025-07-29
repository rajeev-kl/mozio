#!/bin/bash
source /home/ubuntu/.bashrc
CPU_COUNT=$(nproc)
WORKER_COUNT=$(($CPU_COUNT * 3 + 1))
/home/ubuntu/.local/bin/pipenv run gunicorn conf.wsgi:application \
    --bind=127.0.0.1:7100 \
    --workers=$WORKER_COUNT \
    --threads=4 \
    --timeout=20