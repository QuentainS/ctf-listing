#!/usr/bin/env python3
from ics import Calendar
import requests
import arrow
from bcolors import bcolors


def get_calendar():

    url = "https://calendar.google.com/calendar/ical/ctftime%40gmail.com/public/basic.ics"
    return Calendar(requests.get(url).text)


def get_link(ctftime_link):

    # Fetch the webpage (must modify the User Agent)
    html = requests.get(ctftime_link, headers={'User-Agent': 'Mozilla/5.0'})
    html = html.text

    # Sometimes, there are some mistakes in the links
    if "Not found. Back to the" in html:
        return bcolors.fail("404 Error")

    # Get only the interesting part
    start = html.find("Official URL") + 23
    html = html[start:]
    end = html.find("\" rel=\"nofollow\">")
    html = html[:end]

    return html


def parse(event):
    res = {}
    res['name'] = bcolors.colored(event.name, bcolors.BOLD)
    res['start'] = event.begin.to('local')
    res['end'] = event.end.to('local')

    desc = event.description.split('\n')

    if "Jeopardy" in desc[0]:
        res['type'] = bcolors.ok("Jeopardy")  # Love Jeopardy
    elif "Attack-Defense" in desc[0]:
        res['type'] = bcolors.fail("Attack-Defense")  # Hate A-D
    else:
        res['type'] = bcolors.warning(desc[0])  # Oh, something new !

    res['url'] = get_link(desc[1][5:])

    return res


def get_upcoming(calendar, day):

    now = arrow.utcnow().to('local')
    upcoming = []

    # Get the event in [now ; now+day]
    for event in calendar.events:
        if now.shift(days=+day) > event.begin.to('local') > now:
            upcoming.append(parse(event))

    # Sort the events
    upcoming = sorted(upcoming, key=lambda k: k['start'])

    return upcoming


def show(event):
    print(event['start'].humanize())
    print(event['name'])
    print(event['start'])
    print(event['end'])
    print(event['type'])
    print(event['url'])
    print()


if __name__ == "__main__":

    calendar = get_calendar()
    events = get_upcoming(calendar, 15)

    for event in events:
        show(event)
