import requests
import json
import datetime
import re


def date_format(d):
    dt = datetime.datetime.strptime(d, '%Y-%m-%d')
    return dt.strftime('%A %d %B, %Y')


def total_seconds(time):
    lap_regex = re.compile(r'(\d):(\d\d).(\d\d\d)')
    mo = lap_regex.search(time)

    mins = int(mo.group(1))
    secs = int(mo.group(2))
    milli = int(mo.group(3))

    mins *= 60
    milli /= 1000

    return mins + secs + milli

def last_race_results():
    url = 'http://ergast.com/api/f1/current/last/results.json'

    response = requests.get(url)

    if not response.ok:
        return []

    data = json.loads(response.text)

    results_list = []
    race_list = []
    for driver in data['MRData']['RaceTable']['Races'][0]['Results']:
        fn = driver['Driver']['givenName']
        ln = driver['Driver']['familyName']
        url = driver['Driver']['url']
        cons = driver['Constructor']['name']
        points = driver['points']
        pos = driver['position']

        try:
            time = driver['Time']['time']
        except KeyError:  # Times are only given for un-lapped drivers.
            time = driver['status']  # Make time the number of laps behind.
        best_lap = driver['FastestLap']['Time']['time']

        race_info = {'fn': fn, 'ln': ln, 'url': url, 'cons': cons,
                     'points': points, 'pos': pos, 'time': time, 'lap': best_lap}
        race_list.append(race_info)
    results_list.append(race_list)

    round_n = data['MRData']['RaceTable']['Races'][0]['round']
    season = data['MRData']['RaceTable']['Races'][0]['season']
    date = date_format(data['MRData']['RaceTable']['Races'][0]['date'])
    race = data['MRData']['RaceTable']['Races'][0]['raceName']
    circuit = data['MRData']['RaceTable']['Races'][0]['Circuit']['circuitName']
    circuit_url = data['MRData']['RaceTable']['Races'][0]['Circuit']['url']

    circuit_info = {'race': race, 'circuit': circuit, 'url': circuit_url,
                    'round': round_n, 'season': season, 'date': date}
    results_list.append(circuit_info)

    return results_list


def last_quali_results():
    url = 'http://ergast.com/api/f1/current/last/qualifying.json'

    response = requests.get(url)

    if not response.ok:
        return []

    data = json.loads(response.text)

    results_list = []
    quali_list = []
    for driver in data['MRData']['RaceTable']['Races'][0]['QualifyingResults']:
        fn = driver['Driver']['givenName']
        ln = driver['Driver']['familyName']
        url = driver['Driver']['url']
        pos = driver['position']
        try:
            q1 = driver['Q1']  # Drivers may not partake in Q1.
        except KeyError:
            q1 = ''
        try:
            q2 = driver['Q2']  # Drivers eliminated.
        except KeyError:
            q2 = ''
        try:
            q3 = driver['Q3']  # Drivers further eliminated.
        except KeyError:
            q3 = ''

        #  Faster Q2 means negative delta for Q1 delta.
        if q3 is not '':
            q3_time = total_seconds(q3)
            q2_time = total_seconds(q2)
            q1_time = total_seconds(q1)

            q2_delta = round(q2_time - q1_time, 3)
            q3_delta = round(q3_time - q2_time, 3)

        elif q2 is not '':
            q2_time = total_seconds(q2)
            q1_time = total_seconds(q1)
            q3_delta = ''
            q2_delta = round(q2_time - q1_time, 3)

        else:
            q2_delta = ''
            q3_delta = ''

        quali_info = {'fn': fn, 'ln': ln, 'url': url, 'pos': pos, 'q1': q1,
                      'q2': q2, 'q3': q3, 'q2d': q2_delta, 'q3d': q3_delta}
        quali_list.append(quali_info)
    results_list.append(quali_list)

    round_n = data['MRData']['RaceTable']['Races'][0]['round']
    season = data['MRData']['RaceTable']['Races'][0]['season']
    date = date_format(data['MRData']['RaceTable']['Races'][0]['date'])
    race = data['MRData']['RaceTable']['Races'][0]['raceName']
    circuit = data['MRData']['RaceTable']['Races'][0]['Circuit']['circuitName']
    circuit_url = data['MRData']['RaceTable']['Races'][0]['Circuit']['url']

    circuit_info = {'race': race, 'circuit': circuit, 'url': circuit_url,
                    'round': round_n, 'season': season, 'date': date}
    results_list.append(circuit_info)

    return results_list
