from Modules import Greeting, Test, Spotify, HomeAssistant, Webunits
import multiprocessing
import time

class Cmd(object):
    def __init__(self, callables, module, sendCommand):
        """ Command for Voice Assistant
            Parameters:
                - callables -> Words for Recognition
                - module -> Which Module will be called
                - sendCommand -> If the module need the command
        """
        self.callables = callables
        self.module = module
        self.sendCommand = sendCommand

cmds = [
    Cmd(["hallo", "hey", "hi", "moin"], Greeting.greet, True), 
    Cmd(["test"], Test.ausgabe, True),

    # SPOTIFY
    Cmd(["spotify"], Spotify.SP.startPlaying, False),
    Cmd(["pause", "stopp"], Spotify.SP.pause, False),
    Cmd(["überspringen", "nächstes"], Spotify.SP.skip, False),
    Cmd(["play", "spiele"], Spotify.SP.playInQueue, True),
    Cmd(["interpret"], Spotify.SP.getAktArtist, False),
    Cmd(["song", "name"], Spotify.SP.getAktSong, False),

    # HOMEASSISTANT
    Cmd(["zimmer an", "zimmer hell"], HomeAssistant.HA.zimmerAn, False),
    Cmd(["zimmer aus", "zimmer dunkel"], HomeAssistant.HA.zimmerAus, False),
    Cmd(["warmes final", "schreibtisch an", "schreibtischlampe an"], HomeAssistant.HA.schreibTischAn, False),
    Cmd(["lampen aus", "schreibtisch aus", "schreibtischlampe aus"], HomeAssistant.HA.schreibTischAus, False),
    Cmd(["starte pc", "pc an"], HomeAssistant.HA.wakeOnLanTower, False),
    Cmd(["anlage", "steckdose"], HomeAssistant.HA.anlageSwitch, False),

    # WebUntis
    Cmd(["stundenplan"], Webunits.WU.getDayTimeTable, False),
]


def performCommand(main, command):
    thinkThread = multiprocessing.Process(target=main.pixels.think)
    thinkThread.start()
    
    for cmdlist in cmds:
        for cmd in cmdlist.callables:
            if cmd in command:
                response = ""
                if(cmdlist.sendCommand):
                    response = cmdlist.module(command.replace(cmd, ""))
                else:
                    response = cmdlist.module()
                thinkThread.terminate()
                time.sleep(0.2)
                thinkThread.close()


                speakThread = multiprocessing.Process(target=main.pixels.speak)
                speakThread.start()
                if(response != ""):
                    main.VA.talk(response)
                speakThread.terminate()
                time.sleep(0.2)
                speakThread.close()
                

    main.pixels.sleep()