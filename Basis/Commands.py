from Modules import Greeting, Test, Spotify, HomeAssistant, Webunits, NewsAPI, GCalendar, GPeoples
import multiprocessing
import time

class Cmd(object):
    """ Command for Voice Assistant
        Parameters:
            - callables -> Words for Recognition
            - module -> Which Module will be called
            - sendCommand -> If the module need the command
    """
    def __init__(self, callables, module, sendCommand):
        self.callables = callables
        self.module = module
        self.sendCommand = sendCommand

cmds = [
    Cmd(["hallo", "hey", "hi", "moin"], Greeting.G.greet, False), 
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

    # WEBUNTIS
    Cmd(["stundenplan"], Webunits.WU.getDayTimeTable, False),

    # NEWSAPI
    Cmd(["nachrichten zu", "schlagzeilen über"], NewsAPI.NA.getArticlesAbout, True), 
    Cmd(["aktuelle nachrichten"], NewsAPI.NA.getTopArticles, False), 
    Cmd(["aktuelles", "was ist los", "schlagzeilen", "nachrichten"], NewsAPI.NA.getTopHeadlines, False), 
    
    # CALENDAR
    Cmd(["nächster geburtstag"], GCalendar.GC.getNextBirthday, False),
    Cmd(["wann ist wieder"], GCalendar.GC.whenIsNext, True),

    # PEOPLES
    Cmd(["wann hat"], GPeoples.GP.xyBirthday, True),
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
                if(response == None):
                    print("KLICK!")
                elif(response != ""):
                    main.VA.talk(response)
                speakThread.terminate()
                time.sleep(0.2)
                speakThread.close()
    try:            
        thinkThread.terminate()
        thinkThread.close()
    except: pass
    main.pixels.sleep()