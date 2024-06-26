import speech_recognition as sr
# import pyttsx3

import time

from gtts import gTTS
import os
from pydub import AudioSegment
from pydub.playback import play


class VoiceAssistant(object):
    def __init__(self, main):
        self.listener = sr.Recognizer()
        self.listener.dynamic_energy_threshold = True
        self.listener.energy_threshold = 6000
        self.listener.phrase_threshold = 0.2
        self.listener.non_speaking_duration = 0.4
        # self.engine = pyttsx3.init()
        # self.voices = self.engine.getProperty('voices')
        # self.engine.setProperty('voice', self.voices[0].id)

    def talk(self, text):
        print(text)
        # self.engine.say(text)
        # self.engine.runAndWait()

        textArr = text.split("/PAUSE")
        lenTextArr = len(textArr)

        for x in range(lenTextArr):
            if(textArr[x] != ""):
                tts = gTTS(text=textArr[x], lang='de')
                filename = "tmp" + str(x) + ".mp3"
                tts.save(filename)

        for x in range(lenTextArr):
            if(textArr[x] != ""):
                sound = AudioSegment.from_mp3("tmp" + str(x) + ".mp3")
                play(sound.speedup(1.25))
                os.remove("tmp" + str(x) + ".mp3")
                time.sleep(.2)
            else:
                time.sleep(.4)

    def recognition(self, language="de-DE"):
        speech = sr.Microphone()
        with speech as source:
            print("Jetzt sprechen!…")
            self.listener.adjust_for_ambient_noise(source)
            
            try:
                audio = self.listener.listen(source,timeout=10)
            except sr.WaitTimeoutError:
                return ""
        
        try:
            recog = self.listener.recognize_google(audio, language = language).lower()
            print("Erkannt: " + recog)
            return recog
            
        except sr.UnknownValueError:
            print("Google versteht kein Audio")
        except sr.RequestError as e:
            print("Google Service nicht erreichbar; {0}".format(e))