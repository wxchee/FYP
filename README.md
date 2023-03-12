# Rolling Musical Ball

An embedded system equiped with IMU sensor reads orientation data in 3-dimensional space.
By selecting different orientation data as unique input, with each represents a unique musical note, the embedded system can function as a musical instrument.

## Development workflow
Inlcude bin/scripts.sh under .bashsrc to initiate helper command.
```
source <dir to the project>/fyp/bin/scripts.sh
```

<br>
Update host's IP and manually provide client IP which will be used for deploy command.<br>
Note: Make sure to do this everytime the local dev environment connected to a different network, or when RPi's IP is changed.

```
fyp init <RPi IP>
```
<br>

Transfer code to remote RPi's project directory.
```
fyp deploy
```
<br>

Run the program under the local dev environment. 
```
fyp run
```


