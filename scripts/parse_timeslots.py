import json
import os
import pandas as pd
import requests
import sys

URL = 'http://127.0.0.1:5000/{}/'
YEAR = 2019
DATE_FORMAT = '{:02d}/{:02d}/{} {:02d}:{}' # MM/DD/YYYY HH:A
ID_FORMAT = '{}_{}_{}' # POS_DATE_24HOUR

def admin_login():
    payload = {'uid': os.getenv('ADMIN'),
               'pwd': os.getenv('ADMIN_PASS')}
    r = requests.post(URL.format('login'), data=payload)
    return json.loads(r.content.decode())['auth_token']

def post(path, auth_token, **kwargs):
    headers = {'Authorization': auth_token}
    payload = {**kwargs}
    r = requests.post(URL.format(path), data=payload, headers=headers)

    data = json.loads(r.content.decode())
    return data['status'] == 200

def add_position(auth_token, position):
    return post('admin_add_position', auth_token, **{'position': position})

def add_timeslot(auth_token, tsid, position, start, duration, cap):
    return post('admin_add_timeslot', auth_token, **{'tsid': tsid, 'position': position, 'start': start, 'duration': duration, 'cap': cap})

def convert_position(orig):
    return orig.strip().lower().replace(' ', '_')

def convert_start(date, start):
    m, d = date.split('/')
    h, a = start[:-1], start[-1]
    return DATE_FORMAT.format(int(m), int(d), YEAR, int(h), a)

def construct_id(position, date, start):
    d = date.split('/')[1]
    h, a = int(start[:-1]), start[-1]
    h += 12 if a.lower() == 'p' else 0
    return ID_FORMAT.format(position, d, h)

def get_dur_and_cap(payload):
    dur, cap = payload.split(',')
    return int(dur[:-1]), int(cap[:-1])

if __name__ == '__main__':
    auth_token = admin_login()

    filename = sys.argv[1]
    xls = pd.ExcelFile(filename)

    sheet_to_df_map = {}
    for sheet_name in xls.sheet_names:
        sheet_to_df_map[sheet_name] = xls.parse(sheet_name)

    for position, timeslot_df in sheet_to_df_map.items():
        position = convert_position(position)
        add_position(auth_token, position)

        for start_time, row in timeslot_df.iterrows():
            for date in timeslot_df.columns.values:
                data = row[date]
                if type(data) != str:
                    continue
                tsid = construct_id(position, date, start_time)
                start = convert_start(date, start_time)
                dur, cap = get_dur_and_cap(data)

                if add_timeslot(auth_token, tsid, position, start, dur, cap):
                    print('Added timeslot: tsid: {} start: {} dur: {} cap: {}'.format(tsid, start, dur, cap))
                else:
                    print('Failed to add {}'.format(tsid))
    