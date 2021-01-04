from __future__ import print_function
import datetime
import AuthenticationService as authController
import TimetreeService as TTService
from googleapiclient.discovery import build

global glob_event 

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
    for event in events:
        start = event['updated']
    return events  

def googleCalSync():
    lastUpdatedEvents = getLastUpdatedEvents()
    googList = []
    lastUpdate = []

    if glob_event:
        for i in glob_event:
            lastUpdate.append(i['summary'])

    for j in lastUpdatedEvents:
        googList.append(j['summary'])

    deleteFlag = False
    if lastUpdate:
        titleDiff = list(set(lastUpdate) - set(googList))
        for i in titleDiff:
            if i not in googList:
                deleteFlag = True

    # To delete item from TT
    if deleteFlag:
        for i in titleDiff:
            eventId = TTService.findEvent(i)
            code = TTService.deleteEvent(eventId)
            print(code)
    else:
        # To add new item to TT
        eventTTExists = TTService.findEvent(lastUpdatedEvents[0]['summary'])
        if eventTTExists:
            code = TTService.deleteEvent(eventTTExists)
            print(code)
        start = lastUpdatedEvents[0]['start'].get('dateTime', lastUpdatedEvents[0]['start'].get('date'))
        end = lastUpdatedEvents[0]['end'].get('dateTime', lastUpdatedEvents[0]['end'].get('date'))
        res = TTService.createEvent(lastUpdatedEvents[0]['summary'], start, end)
        return 200