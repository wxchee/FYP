
from time import sleep,time
import math
from pysinewave import SineWave
from musicgen import tools
from musicgen.tools import C_Major, STREAM_STATE
import sounddevice as sd
import numpy as np
import sys
import vars


C_major = [0, 2, 4, 5, 7, 9, 11, 12]

prev_time = 0
dt = 0
isPlaying = 0
yawCountDown = 0

class MusicGen:
    def __init__(self):
        self.scales = tools.C_Major
        self.freq = tools.C_Major[0]
        self.goal_freq = tools.C_Major[0]
        
        self.amplitude = 1
        self.goal_amplitude = 1
        
        self.wave = None
        self.wavelength = 0
        self.cross_wave = None
        self.cross_wavele
        self.phase = 0

        self.states = STREAM_STATE.IDLE

        self.fade_duration = 0.5
        # self.states = STREAM_STATE.IDLE
        self.outstream = sd.OutputStream(
            samplerate=tools.fs,
            # blocksize=sd.default.blocksize,
            channels=1,
            callback= lambda *args: self._callback(*args)
        )
        
        self.sinewave = SineWave(pitch=12, pitch_per_second=12)
    def _callback(self, outdata, frames, time, status):
        if (status):
            print('status')
            print(status, sys.stderr)

        if self.states == STREAM_STATE.IDLE:
            if (self.phase + frames >= self.wavelength):
                diff = self.phase + frames - self.wavelength
                new_wave = np.concatenate((self.wave[self.phase:self.wavelength], self.wave[:diff]))
                self.phase = diff
            else:
                new_wave = self.wave[self.phase:(self.phase + frames)]
                self.phase += frames
            pass
        elif self.states == STREAM_STATE.PRECROSSFADE:
            if self.phase + frames >= self.wavelength:
                diff = self.phase + frames - self.wavelength
                new_wave = np.concatenate((self.wave[self.phase:self.wavelength], self.wave[:diff]))
                self.wave = self.cross_wave
                self.phase = diff
            else:
                new_wave = self.wave[self.phase:(self.phase + frames)]
                self.phase += frames
            pass
        elif self.states == STREAM_STATE.PREFADEOUT:
            pass

        # if (self.phase + frames >= self.wave_length):
        #     diff = self.phase + frames - self.wave_length
        #     new_wave = np.concatenate((self.wave[self.phase:self.wave_length], self.wave[:diff]))
        #     self.phase = diff
        # else:
        #     new_wave = self.wave[self.phase:(self.phase + frames)]
        #     self.phase += frames

        outdata[:] = new_wave.reshape(-1,1)

        print('freq {}'.format(self.freq))
        
        # self.phase = (self.phase + frames) % (tools.fs)
    def run(self):
            try:
                # eg. need a wave with eg. 1000 cycles
                self.wavelength = round(tools.fs / C_Major[5] * 10)
                time_array = tools.get_time_array(0, self.wavelength)
                self.wave = tools.get_wave_by_freq(C_Major[5], self.amplitude, time_array)
                self.outstream.start()
                # self.sinewave.play()
                while True:
                    self.set_freq(C_Major[1])
                #     self.sinewave.set_pitch(1)
                #     self.sinewave.set_amplitude(0)
                #     sleep(1)
                #     self.sinewave.set_pitch(2)
                #     sleep(1)
                # self.sinewave.set_amplitude(20)
                # sleep(1)
                # self.sinewave.set_amplitude(0)
                # while True:
                #     print('music thread')
                    # if (self.states == STREAM_STATE.IDLE):
                    #     self.on_idle()
                    # elif (self.states == STREAM_STATE.CROSSFADE):
                    #     self.on_crossfade()
                    # elif (self.states == STREAM_STATE.FADEOUT):
                    #     self.on_fadeout()

                    #-------- C major scale --------#
                    # if (vars.sensor.yaw >= 0 and vars.sensor.yaw < 180):
                    #     i = math.floor(vars.sensor.yaw / 25.7)
                    # else:
                    #     i = 7 - math.floor((vars.sensor.yaw - 180) / 25.7)
                    # print('yaw:{} note:{}'.format(vars.sensor.yaw, i))
                    # self.set_freq(tools.C_Major[i])
                    # sleep(0.05)
            except KeyboardInterrupt:
                print("stop music thread.")

    def on_idle(self):
        pass

    def on_crossfade(self):

        pass

    def on_fadeout(self):
        pass
    
    def set_freq(self, new_freq):
        # let the cross fade sound wave to be 0.5s
        cross_frame = int(0.5 * tools.fs)
        # make sure last frame is a complete cycle to prevent cracking sound
        cross_frame = cross_frame - round(cross_frame % (tools.fs/new_freq)) 
        # new_wave_length = round(tools.fs / new_freq * 10)
        self.goal_freq = new_freq
        time_array = tools.get_time_array(0, cross_frame)
        prev_wave = tools.get_wave_by_freq(self.freq, self.amplitude, time_array)
        next_wave = tools.get_wave_by_freq(new_freq, self.amplitude, time_array)

        cross_env = tools.get_fadeto_env(cross_frame)
        self.cross_wave = prev_wave * cross_env + next_wave * (1-cross_env)
        self.states = STREAM_STATE.PRECROSSFADE
        # if (self.freq != new_freq):
        
            
    # def run_backup(self):
    #     global yawCountDown, isPlaying, dt, prev_time
    #     self.sinewave.play()
    #     isPlaying = 1
    #     i=0
    #     try:
    #         prev_time = time()
    #         print('test music thread')
    #         vol = 0
    #         while True:
    #             dt = time() - prev_time
    #             # print('dt:{} dYaw:{} dYC: {}'.format(dt, vars.sensor.dYaw, yawCountDown))
    #             prev_time = time()
                
    #             # if isPlaying == 1:
    #             #     if (yawCountDown <= 0):
    #             #         # self.sinewave.stop()
    #             #         isPlaying = 0
    #             #         yawCountDown = 0
    #             #     else:
    #             #         yawCountDown = yawCountDown - dt
                    
    #             #     #-------- C major scale --------#
    #             #     if (vars.sensor.yaw >= 0 and vars.sensor.yaw < 180):
    #             #         i = math.floor(vars.sensor.yaw / 25.7)
    #             #     else:
    #             #         i = 7 - math.floor((vars.sensor.yaw - 180) / 25.7)
    #             #     print('yaw:{} note:{}'.format(vars.sensor.yaw, i))
    #             #     self.sinewave.set_pitch(C_major[i])
    #             #     sleep(0.05)

    #             # else:
    #             #     if (vars.sensor.dYaw > 1):
    #             #         yawCountDown = 5 if vars.sensor.dYaw > 50 else vars.sensor.dYaw
    #             #         # self.sinewave.play()
    #             #         isPlaying = 1
                
                
                
    #             # 0-194 [0,12]
    #             # 195-359 [11-1]
    #             # i = math.floor(vars.sensor.yaw / 15) % 13 # range[0, 12]
    #             # if vars.sensor.yaw >= 195 and vars.sensor.yaw < 360:
    #             #     i = 11 - i

    #             # print('test music thread {} {}'.format(vars.sensor.yaw, i))
    #             # self.sinewave.set_pitch(i)

    #             # i = (i + 1) % 8
    #             # self.sinewave.set_pitch(C_major[i])


    #             # #-------- C major scale --------#
    #             # if (vars.sensor.yaw >= 0 and vars.sensor.yaw < 180):
    #             #     i = math.floor(vars.sensor.yaw / 25.7)
    #             # else:
    #             #     i = 7 - math.floor((vars.sensor.yaw - 180) / 25.7)
    #             # print('yaw:{} note:{}'.format(vars.sensor.yaw, i))
    #             # self.sinewave.set_pitch(C_major[i])
    #             # sleep(0.05)
    #     except KeyboardInterrupt:
    #         print("stop music thread.")