#!/bin/bash

echo "fyp run deploy..."

BASEDIR=$(dirname "$0")
echo "basedir: " $BASEDIR

IP_Sensor='192.168.68.116'
# echo "$IP_Sensor"
# scp -v -P 2222 -o ServerAliveInterval=15 -o ServerAliveCountMax=3 -r $BASEDIR/../mball wxchee@$CLIENT_IP:~/
# scp -rp C:/Users/cheew/Documents/fyp/mball wxchee@$CLIENT_IP:~
EXCLUDE_RULES=(--exclude 'fyp/doc' --exclude '__pycache__' --exclude '.git*')
rsync -a --progress --delete-before "${EXCLUDE_RULES[@]}" /home/wxchee/fyp wxchee@$IP_Sensor:~/

echo "deploy completed."