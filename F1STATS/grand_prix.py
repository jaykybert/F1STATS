import requests
import json
from utils import *  # total_seconds and date_format functions.


def race_results():
    """ Get relevant information for the last Formula 1 Race.

    :return driver_dict: A dict containing driver results and round info.
    """
    url = 'http://ergast.com/api/f1/current/last/results.json'

    response = requests.get(url)
    if not response.ok:
        return []

    data = json.loads(response.text)

    driver_list = []
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
            time = driver['status']  # Make time the number of laps behind or retired.

        try:
            best_lap = driver['FastestLap']['Time']['time']
            best_lap_secs = total_seconds(best_lap)
        except KeyError:
            best_lap = '-'
            best_lap_secs = -1
        driver_race_info = {'fn': fn, 'ln': ln, 'url': url, 'cons': cons,
                            'points': points, 'pos': pos, 'time': time, 'bestLap': {'text': best_lap, 'secs': best_lap_secs}}
        driver_list.append(driver_race_info)

    driver_dict = {'Driver': driver_list}

    round_n = data['MRData']['RaceTable']['Races'][0]['round']
    season = data['MRData']['RaceTable']['Races'][0]['season']
    date = date_format(data['MRData']['RaceTable']['Races'][0]['date'])  # Format date.
    race = data['MRData']['RaceTable']['Races'][0]['raceName']
    circuit = data['MRData']['RaceTable']['Races'][0]['Circuit']['circuitName']
    circuit_url = data['MRData']['RaceTable']['Races'][0]['Circuit']['url']

    driver_dict['RoundInfo'] = {'race': race, 'circuit': circuit, 'url:': circuit_url,
                                'round': round_n, 'season': season, 'date': date}
    return driver_dict


def last_quali_results():
    """ Get relevant information for the last Formula 1 Qualifying.

    :return driver_dict: A dict containing driver results and round info.
    """
    url = 'http://ergast.com/api/f1/current/last/qualifying.json'

    response = requests.get(url)
    if not response.ok:
        return []

    data = json.loads(response.text)

    driver_list = []
    for driver in data['MRData']['RaceTable']['Races'][0]['QualifyingResults']:
        fn = driver['Driver']['givenName']
        ln = driver['Driver']['familyName']
        url = driver['Driver']['url']
        pos = driver['position']

        try:
            q1_text = driver['Q1']  # Drivers may not partake in Q1.
            q1_secs = total_seconds(q1_text)
        except KeyError:
            q1_text = ''

        try:
            q2_text = driver['Q2']  # Drivers eliminated in Q1 wont be in Q2.
            q2_secs = total_seconds(q2_text)
        except KeyError:
            q2_text = ''

        try:
            q3_text = driver['Q3']  # Drivers eliminated in Q2 wont be in Q3.
            q3_secs = total_seconds(q3_text)
        except KeyError:
            q3_text = ''

        # Find the delta between qualifying sessions (Q3 - Q2, Q2 - Q1).

        if q3_text is not '':
            q3_secs = total_seconds(q3_text)
            q2_secs = total_seconds(q2_text)
            q1_secs = total_seconds(q1_text)

            q3_delta = round(q3_secs - q2_secs, 3)
            q2_delta = round(q2_secs - q1_secs, 3)

        elif q2_text is not '':
            q2_secs = total_seconds(q2_text)
            q1_secs = total_seconds(q1_text)
            q3_delta = ''
            q2_delta = round(q2_secs - q1_secs, 3)

        else:
            q2_delta = ''
            q3_delta = ''

        # q_sec variables are only used to find fastest lap.
        driver_quali_info = {'fn': fn, 'ln': ln, 'url': url, 'pos': pos, 'q1': {'text': q1_text, 'secs': q1_secs},
                             'q2': {'text': q2_text, 'secs': q2_secs} , 'q3': {'text': q3_text, 'secs': q3_secs}, 'q2d': q2_delta, 'q3d': q3_delta}
        driver_list.append(driver_quali_info)

    driver_dict = {'Driver': driver_list}

    round_n = data['MRData']['RaceTable']['Races'][0]['round']
    season = data['MRData']['RaceTable']['Races'][0]['season']
    date = date_format(data['MRData']['RaceTable']['Races'][0]['date'])  # Format date.
    race = data['MRData']['RaceTable']['Races'][0]['raceName']
    circuit = data['MRData']['RaceTable']['Races'][0]['Circuit']['circuitName']
    circuit_url = data['MRData']['RaceTable']['Races'][0]['Circuit']['url']

    driver_dict['RoundInfo'] = {'race': race, 'circuit': circuit, 'url': circuit_url,
                    'round': round_n, 'season': season, 'date': date}

    return driver_dict


