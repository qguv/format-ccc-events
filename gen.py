import ics
import requests
from datetime import datetime, timezone, timedelta

now = datetime.now(timezone.utc)

c = ics.Calendar(requests.get('https://events.ccc.de/calendar/events.ics').text)

location_overrides = {
    "WHY2025": "Geestmerambacht, Niederlande",
    "38. Chaos Communication Congress": "Hamburg?, Deutschland",
}

flags = {
    'Österreich': '🇦🇹',
    'Serbien': '🇷🇸',
    'Dänemark': '🇩🇰',
    'Niederlande': '🇳🇱',
    'Deutschland': '🇩🇪',
}


def parse_location(event):
    location = location_overrides.get(event.name, event.location)
    pieces = location.split(', ')
    if pieces[-1] not in flags:
        pieces.append('Deutschland')
    flag = flags[pieces[-1]]
    city = pieces[-2].lstrip('0123456789 ')
    return (flag, city)


def parse_dates(event):
    begin = event.begin
    end = event.end - timedelta(days=1)
    if begin.year != end.year:
        return event.begin.strftime('%-d %B %Y') + event.end.strftime('–%-d %B %Y')
    if begin.month != end.month:
        return event.begin.strftime('%-d %B') + event.end.strftime('–%-d %B %Y')
    if begin.day != end.day:
        return event.begin.strftime('%-d') + event.end.strftime('–%-d %B %Y')
    return event.begin.strftime('%-d %B %Y')


for event in c.timeline:
    if event.end < now:
        continue
    flag, city = parse_location(event)
    dates = parse_dates(event)
    print(f'- [{event.name}]({event.url}) ({flag} {city}) {dates}')
