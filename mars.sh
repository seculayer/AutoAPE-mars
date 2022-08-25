#!/bin/bash
######################################################################################
# eyeCloudAI 3.1 MLPS Run Script
# Author : Jin Kim
# e-mail : jinkim@seculayer.com
# Powered by Seculayer © 2021 Service Model Team, R&D Center.
######################################################################################

APP_PATH=/eyeCloudAI/app/ape
####
if [ -x "${APP_PATH}/mars/.venv/bin/python3" ]; then
  PYTHON_BIN="${APP_PATH}/mars/.venv/bin/python3"
else
  PYTHON_BIN="$(command -v python3)"
  export PYTHONPATH=$PYTHONPATH:$APP_PATH/mars/lib:$APP_PATH/mars
  export PYTHONPATH=$PYTHONPATH:$APP_PATH/pycmmn/lib:$APP_PATH/pycmmn
fi

KEY=${1}
WORKER_IDX=${2}

$PYTHON_BIN -m mars.MLAlgRecommender ${KEY} ${WORKER_IDX}
