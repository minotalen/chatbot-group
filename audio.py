from gtts import gTTS
from playsound import playsound

"""
@author Max Petendra
@verion 26.06.20
converts a text to an audio file
--------------
Parameters:
inputtext: The inputtext that sould be converteted to a mp3
audio filename: The audio outplut filename default is given.
"""
def text2audio(inputtext: str = ""):
    text2speach = gTTS(text = inputtext , lang = 'en')
    text2speach.save('currentaudio.mp3') 

"""
@author Max Petendra
@version 26.06.20
Play an mp3 file
----------------
audio_filename: The name of the mp3 file
"""
def playSoundfile():
    playsound('currentaudio.mp3')
