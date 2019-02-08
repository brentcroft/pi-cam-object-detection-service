#!/bin/bash
set -e

sudo ./run-from-cron.sh

sleep 3

tail -f ./service.log
