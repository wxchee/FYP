#!/bin/bash

echo '''
===============================
  fyp command workflow ready.  
===============================
'''

fyp() {
  FILE=/home/wxchee/fyp/bin/commands/$1.sh

  if [ -z $1 ]; then
    echo '''
fyp <command>

Usage:
  fyp init <RPi IP>    generate host'\''s IP and manually provide client IP for later reference
  
  fyp deploy                transfer code to remote RPi'\''s project directory
  fyp run                   start main program and remote client sequentially
  fyp stop                  stop remote client
    

Specify command usages in the scripts.sh file:
  <USERPROFILE>/Documents/fyp/bin/scripts.sh

This is a temporary bash command setup for final year project workflow.
All commands are executed with the leading keyword "fyp".
Command will be removed upon the completion of the project for housekeeping purpose.

To remove the entire fyp <command> series:
remove the config line under
  <USERPROFILE>/.bash_profile

''';

  elif test -f $FILE; then
    $FILE $2 $3
  else
    echo $FILE "does not exist!"
  fi
}

