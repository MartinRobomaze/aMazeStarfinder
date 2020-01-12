#!/usr/bin/env python

import csv
import logging
import os
import requests
import typing

logger = logging.getLogger('') # <--- Probable a good idea to name your logger. '' is the 'root' logger
sysHandler = logging.StreamHandler()
sysHandler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(sysHandler)
logger.setLevel(logging.INFO)

from bs4 import BeautifulSoup

COMMON_STRIP: str = '\n '
ENCODING: str = 'utf-8'
OUTPUT_DIR: str = 'data'
if not os.path.exists(OUTPUT_DIR):
  os.makedirs(OUTPUT_DIR)

url: str = 'https://en.wikipedia.org/wiki/List_of_Messier_objects'
page = requests.get(url)
soup = BeautifulSoup(page.content.decode('utf-8'), 'html.parser')
objects: typing.List[tuple] = []
for tr in soup.find(id='Messier_objects').parent.findNext('table', {'class': 'wikitable'}).findAll('tr'):
  tds: typing.Any = tr.findAll('td')
  if len(tds) == 0:
    continue

  datum: tuple = (
      tds[0].find('a').text.strip(COMMON_STRIP),
      tds[1].text.strip(COMMON_STRIP),
      tds[2].text.strip(COMMON_STRIP),
      f"http:{tds[3].find('img').get('src').strip(COMMON_STRIP)}",
      tds[4].find('a').text,
      tds[5].text.strip(COMMON_STRIP),
      tds[6].text.strip(COMMON_STRIP),
      tds[7].text.strip(COMMON_STRIP),
      tds[8].text.strip(COMMON_STRIP),
      tds[9].text.strip(COMMON_STRIP))
  objects.append(datum)

output_path: str = os.path.join(OUTPUT_DIR, 'messier-objects.csv')
with open(output_path, 'w', newline='\n', encoding=ENCODING) as output_stream:
  writer: csv.writer = csv.writer(output_stream, delimiter=';', lineterminator='\n', quoting=csv.QUOTE_ALL)
  writer.writerow(('Messier number', 'NGC/IC', 'Common name', 'Picture', 'Object Type', 'Distance(kly)', 'Constellation', 'Apparent magnitude', 'Right ascension', 'Declination'))
  for datum in objects:
    writer.writerow(datum)

logger.info(f'CSV Created[{output_path}]')
import sys; sys.exit(0)
