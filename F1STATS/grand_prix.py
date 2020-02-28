import requests
import json
from utils import total_seconds
from utils import date_format


def race_results(round_n=None, season=None):
    """ Get relevant information for a current-year Formula 1 race. If no
    round number is passed, the most-recent race data is provided.

    :param round_n: Round number for the race.
    :param season: The year of the race.
    :return driver_dict: A dict containing driver results and round info.
    """
    if round_n is None:
        if season is None:  # Most-recent race, current season.
            url = 'https://ergast.com/api/f1/current/last/results.json'
        else:  # Most-recent race, specific season.
            url = 'https://ergast.com/api/f1/{}/last/results.json'.format(season)
    else:
        if season is None:  # Specific race, current season.
            url = 'https://ergast.com/api/f1/current/{}/results.json'.format(round_n)
        else:  # Specific race, specific season.
            url = 'https://ergast.com/api/f1/{}/{}/results.json'.format(season, round_n)

    response = requests.get(url)
    if not response.ok:
        return {}

    try:
        data = json.loads(response.text)
        # If the race has not happened yet.
        if not data['MRData']['RaceTable']['Races']:
            return {}

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
                rank = driver['FastestLap']['rank']
            except KeyError:
                best_lap = '-'
                rank = None
            driver_race_info = {'fn': fn, 'ln': ln, 'url': url, 'cons': cons,
                                'points': points, 'pos': pos, 'time': time, 'bestLap': {'text': best_lap, 'rank': rank}}
            driver_list.append(driver_race_info)

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

    except ValueError:
        return {}


def qualifying_results(round_n=None, season=None):
    """ Get relevant information for a current-year Formula 1 qualifying
    session. If no round number is passed, the most-recent qualifying data is provided.

    :param round_n: Round number for the qualifying session.
    :param season: The year of the qualifying session.
    :return driver_dict: A dict containing driver results and round info.
    """
    if round_n is None:
        if season is None:  # Most-recent qualifying, current season.
            url = 'https://ergast.com/api/f1/current/last/qualifying.json'
        else:  # Most-recent qualifying, specific season.
            url = 'https://ergast.com/api/f1/{}/last/qualifying.json'.format(season)
    else:
        if season is None:  # Specific qualifying, current season.
            url = 'https://ergast.com/api/f1/current/{}/qualifying.json'.format(round_n)
        else:  # Specific qualifying, specific season.
            url = 'https://ergast.com/api/f1/{}/{}/qualifying.json'.format(season, round_n)

    response = requests.get(url)
    if not response.ok:
        return {}

    try:
        data = json.loads(response.text)
        # If the race has not happened yet.
        if not data['MRData']['RaceTable']['Races']:
            return {}

        driver_list = []
        for driver in data['MRData']['RaceTable']['Races'][0]['QualifyingResults']:
            fn = driver['Driver']['givenName']
            ln = driver['Driver']['familyName']
            url = driver['Driver']['url']
            pos = driver['position']

            """ The qualifying responses can be empty strings
            as well as simply not existing as keys. I.E. Q1 = '' """
            try:
                q1_text = driver['Q1']  # Drivers may not partake in Q1.
                q1_secs = total_seconds(q1_text)
            except KeyError:
                q1_text = ''
                q1_secs = ''

            try:
                q2_text = driver['Q2']  # Drivers eliminated in Q1 won't be in Q2.
                q2_secs = total_seconds(q2_text)
            except KeyError:
                q2_text = ''
                q2_secs = ''

            try:
                q3_text = driver['Q3']  # Drivers eliminated in Q2 won't be in Q3.
                q3_secs = total_seconds(q3_text)
            except KeyError:
                q3_text = ''
                q3_secs = ''

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
                                 'q2': {'text': q2_text, 'secs': q2_secs}, 'q3': {'text': q3_text, 'secs': q3_secs},
                                 'q2d': q2_delta, 'q3d': q3_delta}
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

    except ValueError:
        return {}
