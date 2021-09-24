
import time
from Basis.Communicate import VoiceAssistant
import Basis.Commands as Command
from Basis.LEDs.pixels import LEDSteuerung

WAKEWORD = "jarvis"
class Jarvis(object):
    def __init__(self):
        self.pixels = LEDSteuerung()
        self.VA = VoiceAssistant(self)

        self.sleepRoutine()

    def sleepRoutine(self):
        while(True):
            recog = self.VA.recognition(language="en-us")
            if recog != None and WAKEWORD in recog:
                self.pixels.wakeup()
                break

        self.recognizeRoutine()

    def recognizeRoutine(self):
        recog = self.VA.recognition(language="de-DE")

        if recog == "":
            self.pixels.sleep()
            self.sleepRoutine()
        elif recog != None:
            Command.performCommand(self, recog)
            self.sleepRoutine()

        self.recognizeRoutine()


J = Jarvis()