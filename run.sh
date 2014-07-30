#!/bin/bash
export SETTINGS='config.DevelopmentConfig'
export SYSTEMOFRECORD_URL=http://0.0.0.0:8000
export REDIS_URL="redis://user:@localhost:6379"
export REDIS_NS_QUEUE_MINT="lr:queue:mint:"

source ./environment.sh
python run_dev.py
