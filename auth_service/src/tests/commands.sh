#!/bin/bash
python3 /tests/functional/utils/wait_for_es.py
python3 /tests/functional/utils/wait_for_redis.py
python3 /tests/functional/utils/wait_for_service.py
cd /tests/functional/
python3 -m pytest