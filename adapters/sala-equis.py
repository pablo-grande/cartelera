#!/usr/bin/env python
# -*- coding: utf-8 -*
import time

from datetime import datetime

from fitz import open as fopen




class SalaEquis:
    location = "SALA EQUIS, C. del Duque de Alba, 4, 28012 Madrid"
    tickets = "https://salaequis.es/taquilla/"
    provider = ""
    sessions = {}

    def set_date(monthday, hour):
        if not ":" in hour:
            hour += ":00"
        ts = time.strptime(f"{hour} {monthday}", "%H:%M %d")
        date = datetime.fromtimestamp(time.mktime(ts))
        return date.replace(month=8, year=2022)

    def fetch_data(self):
        schedule = "sala_equis_08_2022.pdf"
        with fopen(schedule) as pdf:
            pages = [page.get_text() for page in pdf]

        return pages[0].splitlines()


    def __init__(self):
        data = self._fetch_data()
        no_session = "no hay sesiones"
        weekdays = [
            "lunes",
            "martes",
            "miércoles",
            "jueves",
            "viernes",
            "sábado",
            "domingo",
        ]

        for index, line in enumerate(data):
            if (
                any([line.endswith(weekday.upper()) for weekday in weekdays])
                and lines[index + 1] != no_session.upper()
            ):
                monthday = line.split(" ")[0]
                hour, title = lines[index + 1].split("h:")
                self.sessions.update(
                    {
                        set_date(monthday, hour): {
                            "title": title.strip().capitalize()
                        }
                    }
                )
