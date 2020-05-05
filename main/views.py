import datetime
from dateutil import parser
import requests
import uuid

from django.shortcuts import render, redirect
from .models import PermaLinkModel, CustomUserModel

from googleapiclient.discovery import build
from oauth2client import file, client
from social_django.utils import load_strategy


def index(request):
    return render(request, 'main/index.html')


def create_event(request, username, id):
    user = CustomUserModel.objects.get(username=username)

    social = user.social_auth.get(provider='google-oauth2')
    access_token = social.get_access_token(load_strategy())
    credentials = client.AccessTokenCredentials(access_token, 'USER_AGENT')
    service = build('calendar', 'v3', credentials=credentials)
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                      maxResults=100, singleEvents=True,
                                      orderBy='startTime').execute()
    events = events_result.get('items', [])
    disabledDates = []

    for event in events:
        disabledDates.append(event.get('start').get('dateTime')[:10])

    if request.POST:
        date = request.POST.get('date')
        time = request.POST.get('time')
        dt = parser.parse(date+" "+time)
        end_dt = dt + datetime.timedelta(minutes=30)

        event = {
          'summary': 'Meeting with {firstname} {lastname}'.format(firstname=request.POST.get('firstname'), lastname=request.POST.get('lastname')),
          'description': request.POST.get('purpose'),
          'start': {
            'dateTime': '{date}T{time}+05:30'.format(date=str(dt.date()), time=str(dt.time())),
            'timeZone': "Asia/Kolkata",
          },
          'end': {
            'dateTime': '{date}T{time}+05:30'.format(date=str(end_dt.date()), time=str(end_dt.time())),
            'timeZone': "Asia/Kolkata",
           },
          'attendees': [
            {'email': user.email},
            {'email': request.POST.get('email')},
          ],
          'reminders': {
            'useDefault': False,
            'overrides': [
              {'method': 'email', 'minutes': 24 * 60},
            ],
          },
          'sendUpdates': 'all',
        }
        event = service.events().insert(calendarId='primary', body=event).execute()
        return redirect(event.get('htmlLink'))

    context = {
        'username': username,
        'id': id,
        'disabledDates': disabledDates
    }
    return render(request, 'main/create_event.html', context)

def get_permalink(request):
    print(request.user.permalink)
    if request.user.permalink:
        context = {
            'permalink': request.user.permalink
        }
    else:
        permalink_obj = PermaLinkModel()
        permalink_obj.url = 'http://127.0.0.1:8000/{username}/{id}'.format(username=request.user.username, id=request.user.id)
        permalink_obj.save()

        request.user.permalink = permalink_obj
        request.user.save()

        context = {
            'permalink' : permalink_obj.url
        }

    return render(request, 'main/link_page.html', context)
