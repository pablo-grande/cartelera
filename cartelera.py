#!/usr/bin/env python
# -*- coding: utf-8 -*
from adapters import SalaEquis

class Cartelera:
    def request(self):
        pass


class Adapter(Cartelera, SalaEquis):
    def request(self):
        pass


def get_movies(target):
    print(target.request())

