from __future__ import print_function
from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
import datetime
from googleapiclient.discovery import build
import Controllers.GoogleCalendarService as googleService
import Controllers.TimetreeService as TTService
import Controllers.AuthenticationService as authController
import Controllers.MiddlewareService as midService
import uuid
import http.server
import socketserver

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.post("/")
def read_root(request: Optional[str] = None):
    return {"Hello": "World"}

#Use a cron-job to call this hook every month to refresh the Google push notifications channel
@app.post("/<refresh google API hook>")
def renewExpiry(request: Optional[str] = None):
    creds = authController.auth()
    service = build('calendar', 'v3', credentials=creds)

    eventcollect = {
        'id': str(uuid.uuid1()),
        'type': "web_hook",
        'address': "https://changeThis.herokuapp.com/path/to/hook",
        "params": {
            "ttl": 2592000000
        }
    }

    res = service.events().watch(calendarId='primary', body=eventcollect).execute()

@app.post("/<notifications endpoint hook>")
def notification(request: Request):  

    lastUpdatetList = googleService.getLastUpdatedEvents(False)
    currList = googleService.currentList(lastUpdatetList)
    prevList = googleService.prevList()
    code = 0
    
    if len(prevList) > len(currList):
        itemsToDelete = list(set(prevList) - set(currList))  
        code = midService.syncDeleteTTItem(itemsToDelete)
    elif len(currList) > len(prevList):
        itemsToAdd = list(set(currList) - set(prevList))
        code = midService.syncAddTTItem(itemsToAdd, lastUpdatetList)
    elif len(currList) == len(prevList):
        oldName = list(set(prevList) - set(currList))
        newName = list(set(currList) - set(prevList))
        if oldName and newName:
            code = midService.syncUpdateTTItemName(oldName, newName)
        else:
            code = midService.syncUpdateTTItem(lastUpdatetList)
    
    googleService.glob_event = googleService.getLastUpdatedEvents(True)
    return code

@app.get("/<to add>") #google verification html file for registering push notification
async def read_item():
    return RedirectResponse(url="<to add>")