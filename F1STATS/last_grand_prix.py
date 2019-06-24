import requests
import json
import datetime


def last_race_results():
    url = 'http://ergast.com/api/f1/current/last/results.json'

    response = requests.get(url)

    if not response.ok:
        return []

    data = json.loads(response.text)

    results_list = []
    driver_list = []
    for driver in data['MRData']['RaceTable']['Races'][0]['Results']:
        fn = driver['Driver']['familyName']
        ln = driver['Driver']['givenName']
        url = driver['Driver']['url']
        cons = driver['Constructor']['name']
        points = driver['points']
        pos = driver['position']

        try:
            time = driver['Time']['time']
        except KeyError:  # Times are only given for un-lapped drivers.
            time = driver['status']  # Make time the number of laps behind.
        best_lap = driver['FastestLap']['Time']['time']

        driver_info = {'fn': fn, 'ln': ln, 'url': url, 'cons': cons,
                       'points': points, 'pos': pos, 'time': time, 'lap': best_lap}
        driver_list.append(driver_info)
    results_list.append(driver_list)

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


def date_format(d):
    dt = datetime.datetime.strptime(d, '%Y-%m-%d')
    return dt.strftime('%A %d %B, %Y')

