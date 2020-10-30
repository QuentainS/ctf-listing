#!/usr/bin/env python3
from ics import Calendar
import requests
import arrow


def get_calendar():
    url = "https://calendar.google.com/calendar/ical/ctftime%40gmail.com/public/basic.ics"
    return Calendar(requests.get(url).text)


def summarize(event):
    res = {}
    res['name'] = event.name
    res['start'] = event.begin.to('local')
    res['end'] = event.end.to('local')
    res['description'] = event.description
    return res


def get_upcoming(calendar, day):

    now = arrow.utcnow().to('local')
    upcoming = []

    # Get the event in [now ; now+day]
    for event in calendar.events:
        if now.shift(days=+day) > event.begin.to('local') > now:
            upcoming.append(summarize(event))

    # Sort the events
    upcoming = sorted(upcoming, key=lambda k: k['start'])

    return upcoming


calendar = get_calendar()
events = get_upcoming(calendar, 15)

for event in events:
    print(event['start'].humanize())
