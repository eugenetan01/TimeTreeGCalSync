# TimeTreeGCalSync
This web service syncs your Google calendar with your TimeTree Calendar

This REST-ful web service was built on FastAPI using Python.

This runs on Google Calendar API, Google Calendar push notifications and Timetree-sdk

If you'd like to set up your google calendar web hook for push notifications, please refer to this:
https://developers.google.com/calendar/v3/push

After finishing setting up the necessary steps for push notifications, pls add your web hook url to the server.py file and run the script to send a POST request to google API - Google will begin sending watch notifications to your webhook when there are event changes in your calendar.

To start also, please follow this tutorial to generate a credentials.json file and a token.pickle to authenticate your google calendar access:
https://developers.google.com/people/quickstart/python

Please also add 2 fields: "TIMETREETOKEN" and "TIMETREECALENDARID" to the end of the credentials.json file to access your timetree calendar.

To get your time tree token, please follow this documentation:
https://developers.timetreeapp.com/en/docs/api/overview

The Timetree calendar Id you'd like to edit is found in the end of your calendar url like so: https://timetreeapp.com/calendars/<calendar_id>

Please place the credentials.json and the token.pickle and change the file path as per your choosing in the project location 
  - For Heroku deployments, please follow my project structure and place these 2 files in project root

Note:
- Please refer to GlobalStore.json before deploying this project.
- Set up a cron job to call the refresh webhook monthly because the Google Push Notifications channel expires every month. 
