
import time
from Basis.Communicate import VoiceAssistant
import Basis.Commands as Command
from Basis.LEDs.pixels import Pixels, pixels
#import Basis.LEDs.apa102 as apa102

class Jarvis(object):
    def __init__(self):
        # self.VA = VoiceAssistant(self)
        # command = self.VA.take_command()
        command = "Hallo Welt"
        
        Command.performCommand(command)
        


J = Jarvis()