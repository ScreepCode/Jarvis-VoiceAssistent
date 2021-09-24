
import time
from Basis.Communicate import VoiceAssistant
import Basis.Commands as Command
from Basis.LEDs.pixels import LEDSteuerung

WAKEWORD = "jarvis"
class Jarvis(object):
    def __init__(self):
        self.pixels = LEDSteuerung()
        self.VA = VoiceAssistant(self)
        # command = self.VA.take_command()
        # command = "Hallo Welt"
        
        # Command.performCommand(command)

        self.sleep = True
        self.recognize = False

        self.start()
        
    def start(self):
        while True:
            while(self.sleep):
                recog = self.VA.recognition(language="en-us")
                if recog != None and WAKEWORD in recog:
                    self.pixels.wakeup()
                    self.sleep = False
                    self.recognize = True

            while(self.recognize):
                recog = self.VA.recognition(language="de-DE")
                if recog != None:
                    Command.performCommand(self, recog)
                    
                    self.sleep = True
                    self.recognize = False



J = Jarvis()