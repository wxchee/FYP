# Rolling Musical Ball

A embedded system equiped with IMU sensor reads orientation data in 3-dimensional space.
Therefore, by selecting different orientation data as unique input, with each represents a musical note, the embedded system has the potential to be used as a musical instruction.

## Development workflow
### inlcude bin/scripts.sh under .bashsrc to initiate helper command.
```
source <USERPROFILE>/Documents/fyp/bin/scripts.sh
```

### generate host'\''s IP and manually provide client IP for later reference.
```
fyp init <RPi IP>
```

### transfer code to remote RPi's project directory.
```
fyp deploy
```


