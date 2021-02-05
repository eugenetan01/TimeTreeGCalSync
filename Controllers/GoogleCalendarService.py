from __future__ import print_function
import datetime
import Controllers.AuthenticationService as authController
import Controllers.TimetreeService as TTService
from googleapiclient.discovery import build

def getLastUpdatedEvents():
    creds = authController.auth()

    service = build('calendar', 'v3', credentials=creds)
    
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=100,
                                        orderBy='updated').execute()
    events = events_result.get('items', [])
    events = events[::-1]
    if not events:
        print('No upcoming events found.')

    if flag:
        with open("globalStore.json", 'w') as file:
            json.dump(events, file)

    return [] if flag else events

#Get current list of events when webhook was called 
def currentList(lastUpdatedEvents):
    googList = []
    for j in lastUpdatedEvents:
        googList.append(j['summary'])
    return googList

#Get previous list of events before notification web hook was called to check for updates in comparison to currentList
def prevList():
    lastUpdate = []
    with open("globalStore.json") as file:
        glob_event = json.load(file)
        for j in range(len(glob_event)):
            lastUpdate.append(glob_event[j]['summary'])

    return lastUpdate
