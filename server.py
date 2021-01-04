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

def watcher():
    creds = authController.auth()

    service = build('calendar', 'v3', credentials=creds)
    
    eventcollect = {
        'id': str(uuid.uuid1()),
        'type': "web_hook",
        'address': "<to add>"
    }

    res = service.events().watch(calendarId='primary', body=eventcollect).execute()
    print(res)

watcher()