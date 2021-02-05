import Controllers.AuthenticationService as authController
import Controllers.TimetreeService as TTService
import Controllers.GoogleCalendarService as googleService
import json

def syncDeleteTTItem(items):
    code = 500
    for item in items:
        eventTTExists = TTService.findEvent(item)
        if eventTTExists:
            code = TTService.deleteEvent(eventTTExists)
    return code

#Check to see if items to be added are duplicates before adding them to Timetree
def syncAddTTItem(items, lastUpdatedEvents):
    if items:
        code = syncDeleteTTItem(items)

        for index in range(len(items)):
            start = lastUpdatedEvents[index]['start'].get('dateTime', lastUpdatedEvents[index]['start'].get('date'))
            end = lastUpdatedEvents[index]['end'].get('dateTime', lastUpdatedEvents[index]['end'].get('date'))
            res = TTService.createEvent(lastUpdatedEvents[index]['summary'], start, end)
        return 200
    
    else:
        return 500

#Create item in Timetree
def invokeCreateTTItem(event, currStart, currEnd):
    code = 504

    success = TTService.createEvent(event, currStart, currEnd)
    if success: 
        code = 200

    return code

#Update item name in Timetree if only item name was changed in Google Calendar
def syncUpdateTTItemName(oldName, newName):
    code = 500
    code = syncDeleteTTItem(oldName)
    
    for j in newName:
        for i in googleService.getLastUpdatedEvents(False):
            if i['summary'] == j:
                currStart = i['start'].get('dateTime', i['start'].get('date'))
                currEnd = i['end'].get('dateTime', i['end'].get('date'))
                code = invokeCreateTTItem(j, currStart, currEnd)    

    return code 

#Update item in terms of timing if the time has changed in Google calendar
def syncUpdateTTItem(lastUpdatedEvents):
    code = 400
    if lastUpdatedEvents:
        
        with open("globalStore.json") as file:
            glob_event = json.load(file)

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
                        (code, "deleted item in update block")
                        code = invokeCreateTTItem(lastUpdatedEvents[i]['summary'], currStart, currEnd)

    return code
