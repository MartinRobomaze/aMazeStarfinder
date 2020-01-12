import re


class Object:
    def __init__(self, messier, name, type, constellation, ra, dec):
        self.messier = messier
        self.name = name
        self.type = type
        self.constellation = constellation
        self.ra = ra.replace('h', '')
        self.ra = self.ra.replace('m', '')
        self.ra = self.ra.replace('s', '')

        self.dec = dec.replace('°', '')
        self.dec = self.dec.replace('′', '')
        self.dec = self.dec.replace('″', '')
