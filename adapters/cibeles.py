#!/usr/bin/env python
# -*- coding: utf-8 -*
import time
import locale

from datetime import datetime

from bs4 import BeautifulSoup as bs
from icalendar import Calendar, Event
from requests import get


locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

def get_date(date_str):
    date_str = date_str.replace("sept.", "septiembre,")
    date_str = date_str.title()
    ts = time.strptime(date_str, '%A %d De %B, %H:%M')
    date = datetime.fromtimestamp(time.mktime(ts))
    return date.replace(year=2022)


location = "Plaza Cibeles, 1A, 28014 Madrid"
url = "https://www.cibelesdecine.com/es/"
response = get(url)
soup = bs(response.text, 'html.parser')
cal = Calendar()
cal.add("x-wr-timezone", "Europe/Madrid")
movie_list = soup.find_all("div", {"class": "peliculas_listado"})
for movie in movie_list:
    e = Event()
    e.add("summary", "Cine: " + movie.find("div", {"class": "film-list-title"}).text.capitalize())
    e.add("dtstart", get_date(movie.find("div", {"class": "fecha-index"}).text.strip()))
    e.add("description", movie.find("a", {"class": "comprar"})['href'])
    e.add("location", location)
    cal.add_component(e)

with open("cine.ics", "w") as f:
    f.writelines(cal.to_ical().decode())

