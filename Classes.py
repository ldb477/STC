import pyaudio
import wave
import sys

class PlayAudioFile:
    CHUNK = 1024

    def __init__(self, file):
        """ Init audio stream """ 
        self.wf = wave.open(file, 'rb')
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format = self.p.get_format_from_width(self.wf.getsampwidth()),
            channels = self.wf.getnchannels(),
            rate = self.wf.getframerate(),
            output = True
        )

    def play(self):
        """ Play entire file """
        data = self.wf.readframes(self.CHUNK)
        while data != '':
            self.stream.write(data)
            data = self.wf.readframes(self.CHUNK)

    def close(self):
        """ Graceful shutdown """ 
        self.stream.close()
        self.p.terminate()

# Usage example for pyaudio
#a = AudioFile("1.wav")
#a.play()
#a.close()

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

# Usage example for pyaudio
#a = RecordAudioFile("1.wav")
#a.recordInit()
#while(something):
#   a.recordContinue()    
#a.recordStop()

# def list_default_audio_devices(self):

#     recordingDevicesList = r.get_default_input_device_info()
#     playbackDevicesList = p.get_default_output_device_info()

#     print("")

#     for devices in recordingDevicesList:
#         print(devices + " " + str(recordingDevicesList[devices]))

#     print("")

#     for devices in playbackDevicesList:
#         print(devices + " " + str(playbackDevicesList[devices]))

#     print("")