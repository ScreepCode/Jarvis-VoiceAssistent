import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
from time import sleep

SCOPE = "user-read-playback-state,user-modify-playback-state"
MAINDEVICE = "Jarvis Connect"

class Spotify(object):
    def __init__(self):
        self.client = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=SCOPE))

        # songUri = self.getSongUri("Never Gonna Give You Up")
        # self.playTrack(songUri)
        # self.playInQueue(songUri)

        # song = self.getAktSong()
        # artist = self.getAktArtist()

        # device = self.getDeviceID()
        # self.changeDevice(self.getDeviceID())

        # playlistUri(self.getPlaylistUri("Hit Rewind"))
        # self.startPlaylist(playlistUri)

        # self.play()
        # self.pause()
        # self.skip()
        
        # self.startPlaying()

    def play(self):
        self.client.start_playback()

    def pause(self):
        self.client.pause_playback()

    def skip(self):
        self.client.next_track()

    def changeVolume(self, volume):
        self.client.volume(volume)

    def changeDevice(self, deviceID):
        self.client.transfer_playback(deviceID)

    def startPlaying(self):
        self.changeDevice("8bcca50f2032ec0d78734ffa6b4653c170e31981")
        self.play()

    def playTrack(self, name):
        uri = self.getSongUri(name)
        self.client.start_playback(uris=[uri])

    def playInQueue(self, name):
        uri = self.getSongUri(name)
        self.client.add_to_queue(uri)
        self.skip()

    def startPlaylist(self, uri):
        self.client.start_playback(context_uri=uri)

    def getSongUri(self, name):
        results = self.client.search(q=name, limit=1, type="track")
        return results["tracks"]["items"][0]["uri"]

    def getPlaylistUri(self, name):
        results = self.client.search(q=name, limit=1, type="playlist")
        return results["playlists"]["items"][0]["uri"]

    def getAktSong(self):
        track = self.client.current_user_playing_track()['item']
        return track['name']

    def getAktArtist(self):
        track = self.client.current_user_playing_track()['item']
        return (track["artists"][0]["name"])

    def getDeviceID(self, name=MAINDEVICE):
        res = self.client.devices()
        for device in res["devices"]:
            if(device["name"] == name):
                return device["id"]

SP = Spotify()