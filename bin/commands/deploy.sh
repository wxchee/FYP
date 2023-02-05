#!/bin/bash

echo "fyp run deploy..."

BASEDIR=$(dirname "$0")
echo "basedir: " $BASEDIR

CLIENT_IP=`cat < $BASEDIR/../../mball/IP_client.txt`

echo "$CLIENT_IP"
# scp -v -P 2222 -o ServerAliveInterval=15 -o ServerAliveCountMax=3 -r $BASEDIR/../mball wxchee@$CLIENT_IP:~/
# scp -rp C:/Users/cheew/Documents/fyp/mball wxchee@$CLIENT_IP:~
rsync -a --progress --delete-before /home/wxchee/fyp/mball wxchee@$CLIENT_IP:~/

echo "deploy completed."