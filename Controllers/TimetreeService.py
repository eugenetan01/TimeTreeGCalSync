from timetree_sdk import TimeTreeApi
from timetree_sdk.models import events
import Controllers.AuthenticationService as AuthenticationService
import json

api = TimeTreeApi(AuthenticationService.getTimeTreeToken())

def getCalendarId():
    with open('credentials.json') as config_file:
        data = json.load(config_file)
    return data['TIMETREECALENDARID']

def createEvent(summary, start, end):
    calendar = api.get_calendar(getCalendarId())
    event = events.Event(
        data=events.EventData(
            attributes=events.EventAttributes(
                title=summary,
                category='schedule',
                all_day=False,
                start_at=start, 
                end_at=end, 
                description='Description',
                location='Location',
                start_timezone='Singapore',
                end_timezone='Singapore'
            ),
            relationships=events.EventRelationships(
                label=events.EventRelationshipsLabel(
                    data=events.EventRelationshipsLabelData(
                        id='1',
                        type='label'
                    )
                )
            )
        )
    )
    response = api.create_event(getCalendarId(), event)
    
    print(response.data.attributes.title) # Title
    return True

def getALlEvents():
    events = api.get_upcoming_events(getCalendarId(), 'Asia/Singapore', 365)
    return events.data

def deleteEvent(eventId):
    status_code = api.delete_event(getCalendarId(), eventId)
    return status_code

def findEvent(EventName):
    allEvents = getALlEvents()
    for event in allEvents:
        if event.attributes.title == EventName:
            return event.id
    return None 