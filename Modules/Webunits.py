import webuntis
import base64
import datetime
import os

class WebUntis(object):
    def __init__(self, name=os.environ.get("NAME"), vorname=os.environ.get("VORNAME"), klasse=os.environ.get("KLASSE")):
        self.session = webuntis.Session(
                        server = os.environ.get("WEBUNTIS_SERVER"),
                        username = os.environ.get("WEBUNTIS_USERNAME"),
                        password = os.environ.get("WEBUNTIS_PASSWORT"),
                        school = os.environ.get("WEBUNTIS_SCHOOL"),
                        useragent = os.environ.get("WEBUNTIS_USERAGENT")
                    )

        self.session.login()

        self.ID = self.session.get_student(surname=name, fore_name=vorname).id

    def getDayTimeTable(self, start=datetime.date.today(), ende=datetime.date.today()):
        zeiten = ["08:15", "09:00", "10:05", "10:50", "11:55", "12:40", "13:40", "14:30", "15:15"]
        stunden = ["", "", "", "", "", "", "", "", ""]

        table = self.session.timetable(student=self.ID, start=start, end=ende).to_table()

        for _, row in table:
            for _, cell in row:
                for period in cell:
                    startTime = period.start.strftime('%H:%M')
                    stunden[zeiten.index(startTime)] =  (', '.join(su.name for su in period.subjects))
        
        return self.parseSubjectNames(stunden)

    def parseSubjectNames(self, stunden):
        for x in range(len(stunden)):
            if("M-" in stunden[x]):
                stunden[x] = "Mathe"
            elif("D-" in stunden[x]):
                stunden[x] = "Deutsch"
            elif("E-" in stunden[x]):
                stunden[x] = "Englisch"
            elif("IF-" in stunden[x]):
                stunden[x] = "Informatik"
            elif("SW-" in stunden[x]):
                stunden[x] = "SoWi"
            elif("PH-" in stunden[x]):
                stunden[x] = "Physik"
            elif("SP-" in stunden[x]):
                stunden[x] = "Sport"
            elif("GE-" in stunden[x]):
                stunden[x] = "Geschichte"
            elif("ER-" in stunden[x]):
                stunden[x] = "Religion"
            elif("CH-" in stunden[x]):
                stunden[x] = "Chemie"
                
        return stunden

WU = WebUntis()