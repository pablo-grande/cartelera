#!/usr/bin/env python
# -*- coding: utf-8 -*
import time

from datetime import datetime

from icalendar import Calendar, Event
from fitz import open as fopen


today = datetime.today()

def get_date(monthday, hour, month=today.month, year=today.year):
    if ":" not in hour:
        hour += ":00"
    ts = time.strptime(f"{hour} {monthday}", "%H:%M %d")
    date = datetime.fromtimestamp(time.mktime(ts))
    return date.replace(month=month, year=year)


tickets = "https://salaequis.es/taquilla/"
location = "SALA EQUIS, C. del Duque de Alba, 4, 28012 Madrid"
schedule = "sala_equis_03_2023.pdf"
with fopen(schedule) as pdf:
    pages = [page.get_text() for page in pdf]

lines = pages[0].splitlines()

no_session = "no hay sesiones"
weekdays = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]

movies = []
cal = Calendar()
cal.add("x-wr-timezone", "Europe/Madrid")
for index, line in enumerate(lines):
    if (
        any([line.endswith(weekday.upper()) for weekday in weekdays])
        and lines[index + 1] != no_session.upper()
    ):
        monthday = line.split(" ")[0]
        hour, title = lines[index + 1].split("h:")
        e = Event()
        e.add("summary", f"Cine: {title.strip().capitalize()}")
        e.add("dtstart", get_date(monthday, hour))
        e.add("location", location)
        e.add("description", tickets)
        cal.add_component(e)

# with open("sala-equis.ics", "w") as c:
#     c.writelines(cal.to_ical().decode())

