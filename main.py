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
import uuid
import http.server
import socketserver

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.post("/")
def read_root(request: Optional[str] = None):
    return {"Hello": "World"}

@app.post("/<web_hook>")
def notification(request: Request):  

    lastUpdatetList = googleService.getLastUpdatedEvents()
    currList = googleService.currentList(lastUpdatetList)
    prevList = googleService.prevList()
    code = 0
    if len(prevList) > len(currList):
        itemsToDelete = list(set(prevList) - set(currList))  
        code = googleService.syncDeleteTTItem(itemsToDelete)
    elif len(currList) > len(prevList):
        itemsToAdd = list(set(currList) - set(prevList))
        code = googleService.syncAddTTItem(itemsToAdd, lastUpdatetList)
    elif len(currList) == len(prevList):
        oldName = list(set(prevList) - set(currList))
        newName = list(set(currList) - set(prevList))
        if oldName and newName:
            code = googleService.syncUpdateTTItemName(oldName, newName)
        else:
            code = googleService.syncUpdateTTItem(lastUpdatetList)
    
    googleService.glob_event = googleService.getLastUpdatedEvents()
    return code

@app.get("/<to add>") #google verification html file for registering push notification
async def read_item():
    return RedirectResponse(url="<to add>")
