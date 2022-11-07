import numpy
import wave
from random import sample
import pygame
import librosa
import speech_recognition as srec
import openai
from playsound import playsound
from gtts import gTTS
import Classes
import simpleaudio
import pedalboard
import soundfile
from pydub import AudioSegment
#import cohere

#from scipy.io.wavfile import read


t = srec.Recognizer()

openai.api_key = "YOUR-API-KEY"
#co = cohere.Client('YOUR-API-KEY')

start_sequence = "\nSpace Ship Captain:"
restart_sequence = "\n\nSpace Traffic Control:"

#session_prompt = "The following is a conversation with a space ship captain. The ship captain is an old friend of yours.  You were in the intergalactic war together.  The space ship is in a critical state, and their oxygen is running very low.  The space ship captain is about to request permission to dock her space ship at your space station.\n\nSpace Traffic Control: Please request docking permission.\nSpace Ship Captain:"

#session_prompt = "The following is a conversation between a space traffic controller and a space ship captain. The ship captain is trying to smuggle some illegal fruits onto the station.  The space ship captain is about to request permission to dock her space ship at your space station.\n\nSpace Traffic Control: Please request docking permission.\nSpace Ship Captain:"

session_prompt = "The following is a conversation between a space traffic controller and a space ship captain. The space ship captain is about to request permission to dock her space ship at your space station.\n\nSpace Ship Captain: Hello, I would like to request docking permission.\n\nSpace Traffic Control: Please state the name of your ship.\nSpace Ship Captain: The name of my ship is the Constantinople.\n\nSpace Traffic Control: What is the nature of your business at this space station?\nSpace Ship Captain: We are traveling through the area and need to resupply.  We also have some things we may want to trade.\n\nSpace Traffic Control: Please request docking permission.\nSpace Ship Captain:"


chat_log = ''
question = ''
answer = ''

convoAssist = False





def main():

    chat_log = ''


    pygame.init()
    screen = pygame.display.set_mode((240,180))

    spacePressed = False
    spaceReleased = True
    enterPressed = False
    recording = False
    playing = False

    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    spacePressed = True
                    spaceReleased = False

                    #print("Space Bar has been pressed.")

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    spaceReleased = True
                    spacePressed = False

                    #print("Space Bar has been released.")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    enterPressed = True

                    #print("Enter has been pressed.")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    pass


            if event.type == pygame.QUIT:
                running = False




        # If space bar is pressed and not recording
        if spacePressed == True and recording == False:

            blip3Wav = simpleaudio.WaveObject.from_wave_file("blip-3.wav")
            blip3Play = blip3Wav.play()
            blip3Play.wait_done()

            # Begin recording
            r = Classes.RecordAudioFile("output.wav")
            r.recordInit()

            recording = True
            print("Starting Transmission.")

        # If space bar is pressed and recording
        if spacePressed == True and recording == True:
            r.recordContinue()

        # If space bar is released and recording
        if spaceReleased == True and recording == True:

            blip4Wav = simpleaudio.WaveObject.from_wave_file("blip-4.wav")
            blip4Play = blip4Wav.play()
            blip4Play.wait_done()

            # Stop recording
            r.recordStop()
            recording = False
            enterPressed = True
            print("Transmission Stopped.")
            print('')
            

            

        # If enter is pressed
        if enterPressed == True:

            enterPressed = False

            filename = "output.wav"

            with srec.AudioFile(filename) as source:
                # listen for the data (load audio to memory)
                audio_data = t.record(source)
                # recognize (convert from speech to text)
                text = t.recognize_google(audio_data)
                print(f'Space Traffic Control: {text}')

                question = text


            if chat_log == '':
                response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=session_prompt,
                temperature=0.9,
                max_tokens=150,
                top_p=1,
                frequency_penalty=0.0,
                presence_penalty=0.6,
                #stop=["You:", "Captain:"]
                stop=["Space Traffic Control:", "Space Ship Captain:"]
                )

                # response = co.generate( 
                # model='xlarge', 
                # prompt=session_prompt, 
                # max_tokens=50, 
                # temperature=0.9, 
                # k=0, 
                # p=1, 
                # frequency_penalty=0, 
                # presence_penalty=0.6, 
                # stop_sequences=["Space Traffic Control:", "Space Ship Captain:"], 
                # return_likelihoods='NONE') 

                answer = response["choices"][0]["text"]

                #answer = response.generations[0].text

                # Find "\n" from answer string and remove everything afterwards
                location = answer.find('\n')
                if location != -1:
                    print("Location of carriage return = " + str(location))
                    answer = answer[0:location]

                #answer = answer.replace('Space Traffic Control:', '')

                print(f'Space Ship Captain:{answer}')
                print('')

                chat_log = f'{session_prompt}{answer}'


            else:

                prompt_text = f'{chat_log}{restart_sequence}:{question}{start_sequence}:'

                response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=prompt_text,
                temperature=1.0,
                max_tokens=150,
                top_p=1,
                frequency_penalty=0.6,
                presence_penalty=0.6,
                #stop=["You:", "Captain:"]
                stop=["Space Traffic Control:", "Space Ship Captain:"]
                )

                # response = co.generate( 
                # model='xlarge', 
                # prompt=prompt_text, 
                # max_tokens=50, 
                # temperature=0.3, 
                # k=0, 
                # p=0.75, 
                # frequency_penalty=0.75, 
                # presence_penalty=0.75, 
                # stop_sequences=["Space Traffic Control:", "Space Ship Captain:"], 
                # return_likelihoods='NONE') 

                answer = response["choices"][0]["text"]

                #answer = response.generations[0].text

                # Find "\n" from answer string and remove everything afterwards
                location = answer.find('\n')
                if location != -1:
                    print("Location of carriage return = " + str(location))
                    answer = answer[0:location]


                print(f'Space Ship Captain:{answer}')
                print('')

                # if convoAssist == True:
                #     chat_log = f'{chat_log}{answer}'
                # else:
                #     chat_log = f'{chat_log}{answer}{start_sequence}:'

                chat_log = f'{chat_log}{restart_sequence} {question}{start_sequence} {answer}'    

                print(chat_log)


            if len(answer) > 0:
                myobj = gTTS(text=answer, lang='en', slow=False, tld='co.in')
                myobj.save('response.mp3')

                sound = AudioSegment.from_mp3('response.mp3')
                sound.export('responsewav.wav', format="wav")

                y, sr = librosa.load('responsewav.wav', sr=44100)


                hpf = pedalboard.HighpassFilter(cutoff_frequency_hz=2000)
                effected = hpf(y, sample_rate=sr)

                phaser = pedalboard.Phaser(rate_hz=0.5, depth=1.0)
                effected = phaser(effected, sample_rate=sr)

                distortion = pedalboard.Distortion()
                distortion.drive_db = 60
                effected = distortion(effected, sample_rate=sr)

                compressor = pedalboard.Compressor(threshold_db=-20, ratio=25)
                effected = compressor(effected, sample_rate=sr)

            

            soundfile.write('effectedresponsewav.wav', effected, sr, subtype='PCM_24')

            
            blip1Wav = simpleaudio.WaveObject.from_wave_file("blip-1.wav")
            blip1Play = blip1Wav.play()
            blip1Play.wait_done()

            effectedresponsewav = simpleaudio.WaveObject.from_wave_file("effectedresponsewav.wav")
            effectedresponsewavPlay = effectedresponsewav.play()
            effectedresponsewavPlay.wait_done()

            blip2Wav = simpleaudio.WaveObject.from_wave_file("blip-2.wav")
            blip2Play = blip2Wav.play()
            blip2Play.wait_done()
            





if __name__ == "__main__":

    main()


