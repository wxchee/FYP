
import soundfile as sf
from Music3 import SAMPLE_RATE_M3, min_sample_chunk, AUDIO_FILES, SLOT_SIZE, INTERVAL, PERIOD
from Music3.stream import Stream

from multiprocessing import Array
maxOSCount = 60
ds = []
for i in range(maxOSCount):
    ds.append(Array('d', PERIOD))

class MusicTest:
    def __init__(self):
        import sounddevice as sd
        self.ostreams = []
        self.streams = []

        wav, sr = sf.read(AUDIO_FILES[0])

        for i in range(maxOSCount):
            self.streams.append(Stream(wav, SLOT_SIZE * INTERVAL))
            self.ostreams.append(
                sd.OutputStream(samplerate=SAMPLE_RATE_M3,channels=1,blocksize=min_sample_chunk,callback= lambda *args: self._callback(*args, 0)))
    

    def _callback(self, outdata, frames, paT, status, i):
        outdata[:, 0] = self.streams[i].update_wav(ds[i], frames)

    def start(self):
        for i in range(maxOSCount):
            self.ostreams[i].start()

    def stop(self):
        for i in range(maxOSCount):
            self.ostreams[i].close()

    def run(self):
        pass