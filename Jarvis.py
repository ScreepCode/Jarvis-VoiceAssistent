
import time

import Basis.Commands as Command
from Basis.Communicate import VoiceAssistant
from Basis.Communication.Recognition import Recognition
from Basis.LEDs.pixels import LEDSteuerung

WAKEWORD = "jarvis"
class Jarvis(object):
    def __init__(self):
        self.pixels = LEDSteuerung()
        self.VA = VoiceAssistant(self)
        self.Recognition = Recognition()

        self.sleepRoutine()

    def sleepRoutine(self):
        while(True):
            recog = self.Recognition.recognize(type="Tensor")
            if recog != None and WAKEWORD in recog:
                self.pixels.wakeup()
                break

        self.recognizeRoutine()

    def recognizeRoutine(self):
        recog = self.Recognition.recognize(type="Google")

        if recog == "":
            self.pixels.sleep()
            self.sleepRoutine()
        elif recog != None:
            Command.performCommand(self, recog)
            self.sleepRoutine()

        self.recognizeRoutine()


J = Jarvis()
