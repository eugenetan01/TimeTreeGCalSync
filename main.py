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

@app.post("/notifications")
async def notification(request: Request):  
    try:
        code = googleService.googleCalSync()
        print(code)
        return {"status": 200}
    except:
        return {"status": "Error cannot create on Timetree"}
    finally: 
        googleService.glob_event = googleService.getLastUpdatedEvents()

@app.get("/<to add>") #google verification html file for registering push notification
async def read_item():
    return RedirectResponse(url="<to add>")