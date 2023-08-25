# Rolling Musical Ball

An embedded system equiped with IMU sensor to transform object orientation data(gyroscope & acceleromter) into music playback control.


## Command workflow
Inlcude bin/scripts.sh under .bashsrc to setup bash commands that facilitate the workflow.
```
source <dir to the project>/fyp/bin/scripts.sh
```

### fyp init
```
fyp init <RPi IP>
```
Update host's IP and manually provide client(RPI)'s IP which will is needed by `fyp deploy`.

Note: Make sure to do this everytime the local dev environment connected to a different network, or when RPi's IP is changed.

### fyp deploy
```
fyp deploy
```
Command to transfer project's source code to remote RPi's project directory via rsync.


### fyp run
```
fyp run
```
Run the program.


## Play modes
The system has three play modes.

### Mode 1: Melody Sequence playback with rotation speed
As the ball undergoes rotation, a pre-composed sequence of melodies is played. The rotation speed dictates both the speed of playback and the volume of the melodies.

### Mode 2: Blend multiple harmonic streams with orientation data
Three axes are linked to three different instrumental music loops. Users adjust the ball's orientation to activate the corresponding loop.

When the ball's orientation lies between multiple axes, the associated music loops are played concurrently, creating a harmonious blend. Alternatively, to reveal all available instrumental loops at once, user may rotates the ball until its rotation speed exceeds a specified threshold.

### Mode 3: Custom percussive loop
In this mode, six ball orientations correspond to distinct percussive sound effects. Users can create personalized percussive patterns by utilizing these six options.
In this mode, a repeating tempo sound helps users gauge timing. A distinct tick at the loop's end signals its restart. The loop window has a duration of approximately two seconds, divided into 16 slots. Each slot can accommodate up to six percussive sound effects concurrently.

To add a sound effect, user first adjust the chosen sound effect axis upward. They then wait the tempo progress until it reaches the desired slot timing, after which they swiftly twist the axis. The system will detect this twist action and insert the corresponding sound effect into that particular slot.
