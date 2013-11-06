import requests

import os.path
import json
from time import strptime
from calendar import timegm
from datetime import timedelta

WEEK_FILE = '/home/andrew/middlecoin/week.json'
TOTAL_FILE = '/home/andrew/middlecoin/stats.json'
USERS_PATH = '/home/andrew/middlecoin/users'

TOTAL_ORDER = ['totalImmatureBalance', 'totalUnexchangedBalance',
               'totalBalance', 'totalPaidOut', 'totalMegahashesPerSecond',
               'totalRejectedMegahashesPerSecond']
USERS_ORDER = ['immatureBalance', 'unexchangedBalance', 'bitcoinBalance',
               'paidOut', 'megahashesPerSecond', 'rejectedMegahashesPerSecond',
               'lastHourShares', 'lastHourRejectedShares']

TOTAL = object() # sentinel

def convert(x):
  x = float(x)
  if x % 1 == 0:
    x = int(x)
  return x

def write(address, timestamp, report):
  if address is TOTAL:
    path = TOTAL_FILE
    order = TOTAL_ORDER
  else:
    path = os.path.join(USERS_PATH, address + '.json')
    order = USERS_ORDER
  if os.path.exists(path):
    with open(path, 'r') as f:
      history = json.load(f)
  else:
    #print('{} does not exist'.format(path))
    history = []
  output = [convert(report.get(key, 0)) for key in order]
  if not history or history[-1][1:] != output:
    #print('{} has changed'.format(path))
    history.append([timestamp] + output)
    with open(path, 'w') as f:
      json.dump(history, f, separators=(',', ':'))
    if address is TOTAL:
      week = []
      maxdelta = timedelta(days=7)
      for row in history:
        if timedelta(seconds=(timestamp - row[0])) < maxdelta:
          week.append(row)
      with open(WEEK_FILE, 'w') as f:
        json.dump(week, f, separators=(',', ':'))

#print('fetching')
data = requests.get('http://middlecoin.com/json', timeout=10).json()
timestamp = timegm(strptime(data['time'], '%Y-%m-%d %H:%M:%S'))

write(TOTAL, timestamp, data)
for address, rep in data['report']:
  write(address, timestamp, rep)
