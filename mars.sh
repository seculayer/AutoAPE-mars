#!/bin/bash
######################################################################################
# eyeCloudAI 3.1 MLPS Run Script
# Author : Jin Kim
# e-mail : jinkim@seculayer.com
# Powered by Seculayer © 2021 Service Model Team, R&D Center.
######################################################################################

APP_PATH=/eyeCloudAI/app/ape
####
export PYTHONPATH=$PYTHONPATH:$APP_PATH/mars/lib:$APP_PATH/mars
export PYTHONPATH=$PYTHONPATH:$APP_PATH/pycmmn/lib:$APP_PATH/pycmmn

KEY=${1}
WORKER_IDX=${2}

/usr/local/bin/python3.7 -m mars.MLAlgRecommender ${KEY} ${WORKER_IDX}
