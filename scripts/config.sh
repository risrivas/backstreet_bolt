#!/bin/bash

export VERSION=1.0.0.0

export IMAGE_BOLT=backtest_bolt
export SERVICE_BOLT=backtest_bolt

export PROJECT_HOME="$( cd "$(dirname "$0")" ; cd .. ; pwd -P )"
export LOG_DIR="${PROJECT_HOME}/logs"

