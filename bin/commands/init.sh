#!/bin/bash

BASEDIR=$(dirname "$0")

# how to generate IP from linux machine
# https://unix.stackexchange.com/a/402160
IP_DEV=$(ip route get 8.8.8.8 | sed -n '/src/{s/.*src *\([^ ]*\).*/\1/p;q}')
IP_Sensor=$1


sed -i s/IP_DEV='.*\?'/IP_DEV=\'$IP_DEV\'/ $BASEDIR/../../const.py
sed -i s/IP_Sensor='.*\?'/IP_Sensor=\'$IP_Sensor\'/ $BASEDIR/../../const.py

sed -i s/IP_Sensor='.*\?'/IP_Sensor=\'$IP_Sensor\'/ $BASEDIR/deploy.sh


