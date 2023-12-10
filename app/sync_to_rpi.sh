#!/bin/bash
LOCAL_PATH='/home/zhixiang/learningspace/originbot_home_assistant/'
REMOTE_USER='root'
REMOTE_IP='10.11.12.121'
REMOTE_PATH='/root/workspace/originbot_home_assistant/'
rsync -avz $LOCAL_PATH $REMOTE_USER@$REMOTE_IP:$REMOTE_PATH