import pyaudio
import wave


class RecordAudioFile:

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    WAVE_OUTPUT_FILENAME = "output.wav"

    recordingFlag = False
    frames = []

    def __init__(self, file):
        """ Init audio stream """ 
        self.p = pyaudio.PyAudio()
        self.WAVE_OUTPUT_FILENAME = file
        self.stream = self.p.open(format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK
        )
        if len(self.frames) > 0:
            self.frames = []

    def recordInit(self):
        """ Initialize recording """
        #print("INITIALIZING RECORDING")
        self.recordingFlag = True


    def recordContinue(self):
        """ Continue recording """
        #print("CONTINUING RECORDING")
        
        data = self.stream.read(self.CHUNK)
        self.frames.append(data)
        

    def recordStop(self):
        """ Stop recording """
        self.recordingFlag = False
        #print("STOPPED RECORDING")
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()

