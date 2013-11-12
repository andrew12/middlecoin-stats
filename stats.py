import requests

import os.path
import json
from time import strptime
from calendar import timegm
from datetime import timedelta

dirname = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(dirname, 'config.json'), 'r') as f:
  cfg = json.load(f)

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
    path = cfg['total']
    order = TOTAL_ORDER
  else:
    path = os.path.join(cfg['users'], address + '.json')
    order = USERS_ORDER
  if os.path.exists(path):
    with open(path, 'r') as f:
      history = json.load(f)
  else:
    history = []
  output = [convert(report.get(key, 0)) for key in order]
  if not history or history[-1][1:] != output:
    history.append([timestamp] + output)
    with open(path, 'w') as f:
      json.dump(history, f, separators=(',', ':'))
    if address is TOTAL:
      week = []
      maxdelta = timedelta(days=7)
      for row in history:
        if timedelta(seconds=(timestamp - row[0])) < maxdelta:
          week.append(row)
      with open(cfg['week'], 'w') as f:
        json.dump(week, f, separators=(',', ':'))

data = requests.get('http://middlecoin.com/json', timeout=10).json()
timestamp = timegm(strptime(data['time'], '%Y-%m-%d %H:%M:%S'))

write(TOTAL, timestamp, data)
# for address, rep in data['report']:
#   write(address, timestamp, rep)
