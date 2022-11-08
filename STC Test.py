
import pygame
import librosa
import speech_recognition as srec
from gtts import gTTS
import Classes
import pedalboard
import soundfile


# Change these depending on which text generation engine used
# Look for OpenAI/Cohere comments below
import openai
#import cohere


def main():

    t = srec.Recognizer()

    #OpenAI
    openai.api_key = "YOUR-API-KEY"

    #Cohere
    #co = cohere.Client('YOUR-API-KEY')

    start_sequence = "\nSpace Ship Captain:"
    restart_sequence = "\n\nSpace Traffic Control:"
    chat_log = ''
    question = ''
    answer = ''

    #session_prompt = "The following is a conversation with a space ship captain. The ship captain is an old friend of yours.  You were in the intergalactic war together.  The space ship is in a critical state, and their oxygen is running very low.  The space ship captain is about to request permission to dock her space ship at your space station.\n\nSpace Traffic Control: Please request docking permission.\nSpace Ship Captain:"

    #session_prompt = "The following is a conversation between a space traffic controller and a space ship captain. The ship captain is trying to smuggle some illegal fruits onto the station.  The space ship captain is about to request permission to dock her space ship at your space station.\n\nSpace Traffic Control: Please request docking permission.\nSpace Ship Captain:"

    session_prompt = "The following is a conversation between a space traffic controller and a space ship captain. The space ship captain is about to request permission to dock her space ship at your space station.\n\nSpace Ship Captain: Hello, I would like to request docking permission.\n\nSpace Traffic Control: Please state the name of your ship.\nSpace Ship Captain: The name of my ship is the Constantinople.\n\nSpace Traffic Control: What is the nature of your business at this space station?\nSpace Ship Captain: We are traveling through the area and need to resupply.  We also have some things we may want to trade.\n\nSpace Traffic Control: Please request docking permission.\nSpace Ship Captain:"

    pygame.init()
    screen = pygame.display.set_mode((240,180))

    spacePressed = False
    spaceReleased = True
    recordingFinished = False
    recording = False
    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    spacePressed = True
                    spaceReleased = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    spaceReleased = True
                    spacePressed = False

            if event.type == pygame.QUIT:
                running = False



        # If space bar is pressed and not recording - Start Recording
        if spacePressed == True and recording == False:

            playBlip("blip-3.wav")

            # Begin recording
            r = Classes.RecordAudioFile("output.wav")
            r.recordInit()

            recording = True
            print("Starting Transmission.")

        # If space bar is pressed and recording - Continue Recording
        if spacePressed == True and recording == True:
            r.recordContinue()

        # If space bar is released and recording - Stop Recording
        if spaceReleased == True and recording == True:

            playBlip("blip-4.wav")

            # Stop recording
            r.recordStop()
            recording = False
            recordingFinished = True
            print("Transmission Stopped.")
            print('')
            
        # If recording is finished
        if recordingFinished == True:

            recordingFinished = False

            filename = "output.wav"

            # Give the recorded audio to Google to translate to text
            with srec.AudioFile(filename) as source:
                audio_data = t.record(source)
                try:
                    text = t.recognize_google(audio_data)
                    print(f'Space Traffic Control: {text}')
                    question = text
                except:
                    print("No speech heard, try again.")
                    continue

            # If this is the first token to text generation - Get Response Text
            if chat_log == '':

                #OpenAI
                response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=session_prompt,
                temperature=0.9,
                max_tokens=150,
                top_p=1,
                frequency_penalty=0.0,
                presence_penalty=0.6,
                stop=["Space Traffic Control:", "Space Ship Captain:"]
                )

                answer = response["choices"][0]["text"]

                #Cohere
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
                
                #answer = response.generations[0].text
                # Find "\n" from answer string and remove everything afterwards
                # location = answer.find('\n')
                # if location != -1:
                #     print("Location of carriage return = " + str(location))
                #     answer = answer[0:location]
                #answer = answer.replace('Space Traffic Control:', '')


                print(f'Space Ship Captain:{answer}')
                print('')

                chat_log = f'{session_prompt}{answer}'

            # Or if this is not the first token - Get Response Text
            else:

                prompt_text = f'{chat_log}{restart_sequence}:{question}{start_sequence}:'

                #OpenAI
                response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=prompt_text,
                temperature=1.0,
                max_tokens=150,
                top_p=1,
                frequency_penalty=0.6,
                presence_penalty=0.6,
                stop=["Space Traffic Control:", "Space Ship Captain:"]
                )

                answer = response["choices"][0]["text"]

                #Cohere
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

                #answer = response.generations[0].text
                # Find "\n" from answer string and remove everything afterwards
                # location = answer.find('\n')
                # if location != -1:
                #     print("Location of carriage return = " + str(location))
                #     answer = answer[0:location]


                print(f'Space Ship Captain:{answer}')
                print('')

                chat_log = f'{chat_log}{restart_sequence} {question}{start_sequence} {answer}'    

                print(chat_log)

            # If there is text in the response
            if len(answer) > 0:

                # Send text to Google and get generated audio back
                answerSpeech = gTTS(text=answer, lang='en', slow=False, tld='co.in')
                answerSpeech.save('responsewav.wav')

                # Prep the file and do some audio effects
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

                # Save the effected audio file
                soundfile.write('effectedresponsewav.wav', effected, sr, subtype='PCM_24')

                # Play the response audio
                playBlip("blip-1.wav")

                pygame.time.wait(1000)

                pygame.mixer.init()
                res = pygame.mixer.Sound("effectedresponsewav.wav")
                pygame.mixer.Sound.play(res)

                responseLength = pygame.mixer.Sound.get_length(res)
                responseLength = int((responseLength * 1000) + 100)
                pygame.time.wait(responseLength)

                playBlip("blip-2.wav")
            

# Blip player
def playBlip(filename):
    pygame.mixer.init()
    blip = pygame.mixer.Sound(filename)
    pygame.mixer.Sound.play(blip)


if __name__ == "__main__":

    main()


