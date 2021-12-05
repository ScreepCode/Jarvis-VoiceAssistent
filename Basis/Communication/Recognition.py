import os
import time
import wave

import speech_recognition as sr
from Basis.Communication.ProcessTensor import ProcessTensor
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play


class Recognition(object):
    def __init__(self):
        self.listener = sr.Recognizer()
        self.listener.dynamic_energy_threshold = True
        self.listener.energy_threshold = 6000
        self.listener.phrase_threshold = 0.2
        self.listener.non_speaking_duration = 0.4

        self.proTensor = ProcessTensor()

        time.sleep(0.2)

    def recognize(self, type="Google"):
        speech = sr.Microphone(sample_rate=48000)
        with speech as source:
            print("Jetzt sprechen!…")
            self.listener.adjust_for_ambient_noise(source)
            
            try:
                audio = self.listener.listen(source,timeout=20)
            except sr.WaitTimeoutError:
                return ""

        if(type == "Google"):
            recog = self.processGoogle(audio)
        elif(type == "Tensor"):
            recog = self.processTensor(audio)

        return recog

    def processGoogle(self, audio):
        try:
            recog = self.listener.recognize_google(audio, language = "de-DE").lower()
            print("Erkannt: " + recog)
            return recog
            
        except sr.UnknownValueError:
            print("Google versteht kein Audio")
        except sr.RequestError as e:
            print("Google Service nicht erreichbar; {0}".format(e))

    def processTensor(self, audio):
        try:
            wav_writer = wave.open("/home/pi/Jarvis/Basis/Communication/ModelSave/tmp.wav", "wb")
            try:  # note that we can't use context manager, since that was only added in Python 3.4
                wav_writer.setframerate(48000.0)
                wav_writer.setsampwidth(2)
                wav_writer.setnchannels(1)
                wav_writer.writeframes(audio.get_raw_data())
            finally:
                wav_writer.close()
            time.sleep(2)

            return self.proTensor.predict()

        except Exception as e:
            print(e)
