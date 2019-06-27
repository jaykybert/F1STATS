import requests
import json
import datetime     # Date formatting.
import re           # Extracting parts of a lap time (mins/secs/milli).
import pprint


def date_format(d):
    """ Format the date appropriately for output.

    :param d: Date - I.E. 2019-12-31
    :return: Date - I.E. Tuesday 31 December 2019
    """
    dt = datetime.datetime.strptime(d, '%Y-%m-%d')
    return dt.strftime('%A %d %B, %Y')


def total_seconds(time):
    """ Get a lap time in the form of seconds.

     :param time: Lap time - I.E. 1:27.809
     :return: The lap time in seconds."""

    """ I used a regular expression for this due to the (very unlikely) possibility
     that a lap is 10 minutes or more, otherwise string slicing would work. """
    lap_regex = re.compile(r'(\d+):(\d\d).(\d\d\d)')

    mo = lap_regex.search(time)

    mins = int(mo.group(1))
    secs = int(mo.group(2))
    milli = int(mo.group(3))
    mins *= 60
    milli /= 1000
    return mins + secs + milli


def last_race_results():
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

        best_lap = driver['FastestLap']['Time']['time']
        best_lap_secs = total_seconds(best_lap)

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

    pprint.pprint(data)
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
            q1 = ''

        try:
            q2_text = driver['Q2']  # Drivers eliminated in Q1 wont be in Q2.
            q2_secs = total_seconds(q2_text)
        except KeyError:
            q2 = ''

        try:
            q3_text = driver['Q3']  # Drivers eliminated in Q2 wont be in Q3.
            q3_secs = total_seconds(q3_text)
        except KeyError:
            q3 = ''

        # Find the delta between qualifying sessions (Q3 - Q2, Q2 - Q1).
        if q3 is not '':
            q3_time = total_seconds(q3)
            q2_time = total_seconds(q2)
            q1_time = total_seconds(q1)

            q3_delta = round(q3_time - q2_time, 3)
            q2_delta = round(q2_time - q1_time, 3)

        elif q2 is not '':
            q2_time = total_seconds(q2)
            q1_time = total_seconds(q1)
            q3_delta = ''
            q2_delta = round(q2_time - q1_time, 3)

        else:
            q2_delta = ''
            q3_delta = ''

        driver_quali_info = {'fn': fn, 'ln': ln, 'url': url, 'pos': pos, 'q1': {'text': q1_text, 'secs': q1_text},
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
