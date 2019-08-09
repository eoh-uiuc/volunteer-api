import click
import csv
import datetime
import re
import os

from pymongo import MongoClient

class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

client = MongoClient(os.environ['MONGO_URI'])

@click.group()
def cli():
  pass

@click.command()
def all_users():
  db=client.users_db
  users = db.users.find()

  with open('volunteers.csv', 'w') as csvfile:
      fieldnames = ['uid', 'name', 'phone', 'society']
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

      writer.writeheader()

      for u in users:
        if len(u['timeslots']) > 0:
          del u['_id']
          del u['pass_hash']
          del u['timeslots']
          if not re.match(r'.*@illinois.edu$', u['uid']):
            u['uid'] = u['uid'] + '@illinois.edu'
          writer.writerow(u)

@click.command()
def today():
  today = datetime.datetime.today().strftime('%m/%d/%Y')

  times_db = client.times_db
  times = times_db.slots.find()

  users = set()
  for t in times:
    date = t['start'].split(' ')[0]
    if (date == today):
      for u in t['registered']:
        users.add(u)

  with open('today.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['uid'])
    for uid in users:
      uid = uid.strip()
      if not re.match(r'.*@illinois.edu$', uid):
        uid = uid + '@illinois.edu'
      writer.writerow({ 'uid': uid.lower() })

def gather_times(user):
  if user is None:
    return 0

  acc = 0
  checkins = user['checkin_times']
  checkouts = user['checkout_times']

  for checkin, checkout in zip(checkins, checkouts):
    acc += int(checkout) - int(checkin)

  return acc

def truncate(f, n):
  '''Truncates/pads a float f to n decimal places without rounding'''
  s = '{}'.format(f)
  if 'e' in s or 'E' in s:
      return '{0:.{1}f}'.format(f, n)
  i, p, d = s.partition('.')
  return '.'.join([i, (d+'0'*n)[:n]])

@click.command()
@click.argument('name')
def society(name):
  users_db = client.users_db
  hours_db = client.hours_db

  users = users_db.users.find({ 'society': name })

  acc = 0
  for u in users:
    uid = u['uid']
    slot = hours_db.slots.find_one({ 'uid': uid })
    t = float(truncate(gather_times(slot) / 3.6e6, 3))
    print(f'{bcolors.OKBLUE}{uid}{bcolors.ENDC}: {t} H')
    acc += t

  print(f'{bcolors.HEADER}Total hours{bcolors.ENDC}: {acc} HOURS')

@click.command()
@click.argument('outputFile')
def all_hours(outputfile):
  db = client.users_db
  hours_db  = client.hours_db
  users = db.users.find()

  with open(outputfile, 'w') as csvfile:
      fieldnames = ['uid', 'name', 'phone', 'society', 'hours']
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

      writer.writeheader()

      for u in users:
        if len(u['timeslots']) > 0:
          del u['_id']
          del u['pass_hash']
          del u['timeslots']

          uid = u['uid']
          slot = hours_db.slots.find_one({ 'uid': uid })
          t = float(truncate(gather_times(slot) / 3.6e6, 3))
          if t == 0:
            continue

          u['hours'] = t

          if not re.match(r'.*@illinois.edu$', u['uid']):
            u['uid'] = u['uid'] + '@illinois.edu'
          writer.writerow(u)

cli.add_command(all_users)
cli.add_command(today)
cli.add_command(society)
cli.add_command(all_hours)

if __name__ == '__main__':
  cli()
