from requests import get, post
import os

IP = "http://192.168.178.28:8123" 

class HomeAssistant(object):
    def __init__(self):
        self.headers = {"Authorization" : os.environ.get("HOMEASSISTANT_TOKEN"), "content-type": "application/json"}

    def scenes(self, sceneID):
        data = {
            "entity_id": "scene." + sceneID
        }
        url = IP + "/api/services/homeassistant/turn_on"
        post(url, headers=self.headers, json=data)

    def scripts(self, scriptID):
        url = IP + "/api/services/script/" + scriptID
        post(url, headers=self.headers)

    def device(self, entityID):
        url = IP + "/api/services/light/toggle"
        data = {
            "entity_id": "light." + entityID
        }
        post(url, headers=self.headers, json=data)


    def zimmerAn(self):
        self.scenes("zimmer_an")

    def zimmerAus(self):
        self.scenes("zimmer_aus")

    def schreibTischAn(self):
        self.scripts("warmes_final")

    def schreibTischAus(self):
        self.scripts("lampen_aus")

    def wakeOnLanTower(self):
        self.scripts("pc_wake_on_lan")

    def anlageSwitch(self):
        self.device("on_off_plug_1")


HA = HomeAssistant()
        