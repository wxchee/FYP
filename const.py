IP_DEV='192.168.68.124'
IP_Sensor='192.168.68.119'
SERVER_PORT=4010
BUFFER_SIZE=1024
SERVER_ADDR_PORT=(IP_DEV, SERVER_PORT)


# note_freqs = [261.63 * pow(2, i/12) for i in range(12)]
NOTES = [
    261.63,     # C     
    277.187,    # C#
    293.67,     # D
    311.132,    # D#
    329.633,    # E
    349.234,    # F
    370.001,    # F#
    392.002,    # G
    415.312,    # G#
    440.007,    # A
    466.172,    # A#
    493.892     # B
]

SAMPLING_RATE=22050
CHANNELS = 2