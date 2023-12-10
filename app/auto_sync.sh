#!/bin/bash
LOCAL_PATH='/home/zhixiang/learningspace/originbot_home_assistant/'
inotifywait -m -e close_write $LOCAL_PATH | while read dir action file; do
    /home/zhixiang/learningspace/originbot_home_assistant/app/sync_to_rpi.sh
done