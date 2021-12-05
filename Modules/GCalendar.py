from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class GCalendar(object):
    def __init__(self):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        self.service = build('calendar', 'v3', credentials=creds)
        self.calendarList = self.getCalendarList()

    
    def getNextBirthday(self):  #MOVE TO PEOPLES API? Eher nicht
        event = self.getCalendarEvents("addressbook#contacts@group.v.calendar.google.com", 1, True)[0]
        name = event["summary"].replace(" hat Geburtstag", "")
        datum = event['start'].get('dateTime', event['start'].get('date')).split("-")
        
        tag =  datum[2]+ "."
        monat = datetime.datetime.strptime(datum[1], "%m").strftime("%B")

        return "Als nächstes hat " + name + " am " + tag + monat + " Geburtstag."


    def xyBirthday(self, name):  #MOVE TO PEOPLES API? -> Empfelenswert
        events = self.getCalendarEvents("addressbook#contacts@group.v.calendar.google.com", 1000, True)
        for event in events:
            if(name in event['summary'].lower()):
                datum = event['start'].get('dateTime', event['start'].get('date')).split("-")
        
                tag =  datum[2]+ "."
                monat = datetime.datetime.strptime(datum[1], "%m").strftime("%B")
        
                return name + " hat am " +  tag + monat + " Geburtstag."
        
        return "Name nicht gefunden"

    def whenIsNext(self, name):  
        calendarID = None
        for calendar in self.calendarList:
            if calendar[0] == name:
                calendarID = calendar[1]
        
        if calendarID != None:
            termine = self.getCalendarEvents(calendarID, 1, True)
            if len(termine) > 0:
                termin = termine[0]["summary"]
            else:
                return "Es gibt keine nächsten Termine in: " + name

            return "Nächster Termin in " + name + ": " + termin
        
        else:
            return "Es gibt den Kalendar " + name + " nicht"

    def getCalendarList(self):
        result = []
        page_token = None
        while True:
            calendar_list = self.service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                result.append([calendar_list_entry['summary'], calendar_list_entry['id']])
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break
        return result

    def getCalendarEvents(self, calendarID, maxResults, singleEvents):
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        events_result = self.service.events().list(calendarId=calendarID, timeMin=now,
                                            maxResults=maxResults, singleEvents=singleEvents,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])
        return events

GC = GCalendar()