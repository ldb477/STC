# STC
Space Traffic Control

This just a tech demo proof of concept for a space game where you (the Space Traffic Controller) must communicate over a walkie-talkie type comms channel with a space ship captain in order to learn more about who they are and what is on their ship.  Because this is using OpenAI's GPT3 text generation, you can have a lot of fun with what you and the space ship captain talk about.  You can even make a new prompt that gives the ship's captain an ulterior motive.


To Play:

- Install the required libraries
- Get an API key from OpenAI (you can get one with a free trial) and enter it into the top of __main__ where it says YOUR_API_KEY.  If you want to use Cohere you can, you will need to comment out OpenAI code and comment in Cohere code.  The Cohere values are not as dialed in, so results may vary.
- Make sure you have speakers and a microphone
- Run the program
- When the blank window pops up, press and hold down the space bar to talk
- Wait for a response from the ship's captain, and press and hold the space bar to respond

```
Library Dependencies:

pygame
librosa
speechrecognition
gtts
pedalboard
soundfile
openai OR cohere  <-- OpenAI is used by default, but Cohere can be commented in if desired
pyaudio
wave
```
