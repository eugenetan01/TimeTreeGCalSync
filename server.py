from __future__ import print_function
from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
import datetime
from googleapiclient.discovery import build
import Controllers.AuthenticationService as authController
import uuid
import http.server
import socketserver

#Run this script once locally to set up the notification webhook to your webapp
def watcher():
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

watcher()