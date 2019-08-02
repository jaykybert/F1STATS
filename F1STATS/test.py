import requests
import json
import pprint
import re
from utils import *

""" A test to try and get deltas between drivers, as opposed to between qualifying runs."""




def qualifying_results(round_n=None):
    """ Get relevant information for a current-year Formula 1 qualifying
    session. If no round number is passed, the most-recent qualifying data is provided.

    :param round_n: Round number for the qualifying session..
    :return driver_dict: A dict containing driver results and round info.
    """
    if round_n is None:
        url = 'http://ergast.com/api/f1/current/last/qualifying.json'
    else:
        url = 'http://ergast.com/api/f1/current/{}/qualifying.json'.format(round_n)

    response = requests.get(url)
    if not response.ok:
        return []

    try:
        data = json.loads(response.text)

        # If the race has not happened yet.
        if not data['MRData']['RaceTable']['Races']:
            return []

        driver_list = []
        q3_list = []
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

            try:
                q2_text = driver['Q2']  # Drivers eliminated in Q1 won't be in Q2.
                q2_secs = total_seconds(q2_text)
            except KeyError:
                q2_text = ''

            try:
                q3_text = driver['Q3']  # Drivers eliminated in Q2 won't be in Q3.
                q3_secs = total_seconds(q3_text)
                q3_list.append(q3_secs)
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
                                 'q2': {'text': q2_text, 'secs': q2_secs}, 'q3': {'text': q3_text, 'secs': q3_secs}, 'q2d': q2_delta, 'q3d': q3_delta}
            driver_list.append(driver_quali_info)

        driver_dict = {'Driver': driver_list}

        round_n = data['MRData']['RaceTable']['Races'][0]['round']
        season = data['MRData']['RaceTable']['Races'][0]['season']
        date = date_format(data['MRData']['RaceTable']['Races'][0]['date'])  # Format date.
        race = data['MRData']['RaceTable']['Races'][0]['raceName']
        circuit = data['MRData']['RaceTable']['Races'][0]['Circuit']['circuitName']
        circuit_url = data['MRData']['RaceTable']['Races'][0]['Circuit']['url']

        driver_dict['RoundInfo'] = {'race': race, 'circuit': circuit, 'url': circuit_url,
                                    'round': round_n, 'season': season, 'date': date, 'gap': {'Q3': q3_list}}

        return driver_dict

    except ValueError:
        return []

def gap_to(q_list):
    gap_list = []
    for i in range(len(q_list)):
        try:
            gap = round(q_list[i+1] - q_list[i], 3)
            gap_list.append(gap)
        except IndexError:  # No time.
            pass

    return gap_list

q_results = qualifying_results()

q_list = gap_to(q_results['RoundInfo']['gap']['Q3'])


for i in range(len(q_list)):

    q_results['Driver'][i]['Delta'] = q_list[i]

    pprint.pprint(q_results['Driver'])



