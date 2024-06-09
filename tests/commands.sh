#!/bin/bash
python3 /tests/utils/wait_for_redis.py
python3 /tests/utils/wait_for_postgres.py
python3 /tests/utils/wait_for_service.py
cd /tests/
python3 -m pytest