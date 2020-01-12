#!/usr/bin/env python

'''
To run this script, please use pipenv, conda, or venv and install the following packages.

$ pip install pandas requests
'''
import logging
import os
import pandas
import requests

logger = logging.getLogger('') # <--- Probable a good idea to name your logger. '' is the 'root' logger
sysHandler = logging.StreamHandler()
sysHandler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(sysHandler)
logger.setLevel(logging.INFO)

CHUNK_SIZE: int = 1024
ENCODING: str = 'utf-8'
OUTPUT_DIR: str = '/tmp/outputs'
if not os.path.exists(OUTPUT_DIR):
  os.makedirs(OUTPUT_DIR)

url: str = 'https://raw.githubusercontent.com/jbcurtin/messier-catalogue/master/data/messier-objects.csv'
filename: str = os.path.basename(url.rsplit('?', 1)[0])
filepath: str = os.path.join(OUTPUT_DIR, filename)
with open(filepath, 'wb') as output_stream:
  logger.info(f'Downloading Data[{filename}]')
  response = requests.get(url, stream=True)
  for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
    output_stream.write(chunk)

data_frame: pandas.core.frame.DataFrame = pandas.read_csv(filepath, delimiter=';')
print(data_frame)

