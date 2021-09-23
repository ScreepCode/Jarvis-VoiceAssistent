from Modules import Greeting, Test, Spotify, HomeAssistant, Webunits


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


def performCommand(command):
    for cmdlist in cmds:
        for cmd in cmdlist.callables:
            if cmd in command:
                if(cmdlist.sendCommand):
                    cmdlist.module(command.replace(cmd, ""))
                else:
                    cmdlist.module()