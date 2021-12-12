from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly", "https://www.googleapis.com/auth/contacts.readonly"]

class GPeople(object):
    def __init__(self):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('GoogleCredentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        self.service = build('people', 'v1', credentials=creds)

    def xyBirthday(self, name):
        peopleWithBirthdayEntry = self.getAllBirthdays()
        for people in peopleWithBirthdayEntry:
            if(name.replace("geburtstag", "").strip() in people[0].lower()):
                birthday = people[1]
                if((datetime.datetime.now() - birthday).days > 0):
                    alter = str(int(datetime.datetime.strftime(datetime.datetime.now(), "%Y")) - int(datetime.datetime.strftime(birthday, "%Y")) + 1) 
                else: 
                    alter = str(int(datetime.datetime.strftime(datetime.datetime.now(), "%Y")) - int(datetime.datetime.strftime(birthday, "%Y")))
                return people[0] + " wird am " +  datetime.datetime.strftime(birthday, "%d") + ". " + datetime.datetime.strftime(birthday, "%B") + " " + alter + " alt."

        return ""

    def getAllPeople(self):
        results = self.service.people().connections().list(
            resourceName='people/me',
            pageSize=1000,
            sortOrder="FIRST_NAME_ASCENDING",
            personFields='names,birthdays').execute()
        return results.get('connections', [])

    def getAllBirthdays(self):
        peoples = self.getAllPeople()
        result = []
        for person in peoples:
            names = person.get('names', [])
            birthday = person.get("birthdays")
            if names:
                if(birthday):
                    name = names[0].get('displayName')
                    birthday = birthday[0].get('date')
                    birthday = datetime.datetime(birthday["year"], birthday["month"], birthday["day"])
                    result.append([name, birthday])

        return result


GP = GPeople()