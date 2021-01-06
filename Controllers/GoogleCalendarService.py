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
    for event in events:
        start = event['updated']
        print(start, event['summary'])

    return events  

glob_event = getLastUpdatedEvents()

def currentList(lastUpdatedEvents):
    googList = []
    for j in lastUpdatedEvents:
        googList.append(j['summary'])
    return googList

def prevList():
    lastUpdate = []
    if glob_event:
        for i in glob_event:
            lastUpdate.append(i['summary'])
    else:
        print("nothing to show in glob event")
    return lastUpdate

def syncDeleteTTItem(items):
    code = 500
    for item in items:
        eventTTExists = TTService.findEvent(item)
        if eventTTExists:
            code = TTService.deleteEvent(eventTTExists)
    return code

def syncAddTTItem(items, lastUpdatedEvents):
    if items:
        res = syncDeleteTTItem(items)
    
        for index in range(len(items)):
            start = lastUpdatedEvents[index]['start'].get('dateTime', lastUpdatedEvents[index]['start'].get('date'))
            end = lastUpdatedEvents[index]['end'].get('dateTime', lastUpdatedEvents[index]['end'].get('date'))
            res = TTService.createEvent(lastUpdatedEvents[index]['summary'], start, end)
        
        return res
    
    else:
        return 500

def invokeCreateTTItem(event, currStart, currEnd):
    code = 504

    success = TTService.createEvent(event, currStart, currEnd)
    if success: 
        code = 200
        
    return code

def syncUpdateTTItemName(oldName, newName):
    code = 500
    code = syncDeleteTTItem(oldName)
    
    for j in newName:
        for i in getLastUpdatedEvents():
            if i['summary'] == j:
                currStart = i['start'].get('dateTime', i['start'].get('date'))
                currEnd = i['end'].get('dateTime', i['end'].get('date'))
                code = invokeCreateTTItem(j, currStart, currEnd)    

    return code 

def syncUpdateTTItem(lastUpdatedEvents):
    code = 400
    if lastUpdatedEvents:
        for i in range(len(lastUpdatedEvents)):
            for j in range(len(glob_event)):
                flag = False
                if lastUpdatedEvents[i]['summary'] == glob_event[j]['summary']:
                    currStart = lastUpdatedEvents[i]['start'].get('dateTime', lastUpdatedEvents[i]['start'].get('date'))
                    prevStart = glob_event[j]['start'].get('dateTime', glob_event[j]['start'].get('date'))

                    currEnd = lastUpdatedEvents[i]['end'].get('dateTime', lastUpdatedEvents[i]['end'].get('date'))
                    prevEnd = lastUpdatedEvents[j]['end'].get('dateTime', lastUpdatedEvents[j]['end'].get('date'))
                    if currStart != prevStart or currEnd != prevEnd:
                        flag = True
                if flag:
                    code = syncDeleteTTItem([lastUpdatedEvents[i]['summary']])
                    code = invokeCreateTTItem(lastUpdatedEvents[i]['summary'], currStart, currEnd)

    return code
