import requests
import json
from utils import total_seconds
from utils import date_format


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

        """ 
        The loop uses range instead of foreach because it references the previous
        driver's qualifying time by index[i-1] to compare them.
        """
        driver_list = []
        for i in range(len(data['MRData']['RaceTable']['Races'][0]['QualifyingResults'])):

            fn = data['MRData']['RaceTable']['Races'][0]['QualifyingResults'][i]['Driver']['givenName']
            ln = data['MRData']['RaceTable']['Races'][0]['QualifyingResults'][i]['Driver']['familyName']
            url = data['MRData']['RaceTable']['Races'][0]['QualifyingResults'][i]['Driver']['url']
            pos = data['MRData']['RaceTable']['Races'][0]['QualifyingResults'][i]['position']

            try:  # Drivers may not partake in Q1.
                q1_text = data['MRData']['RaceTable']['Races'][0]['QualifyingResults'][i]['Q1']
                q1_secs = total_seconds(q1_text)
            except KeyError:
                q1_text = '-'
                q1_secs = '-'

            try:  # Drivers eliminated in Q1 won't be in Q2.
                q2_text = data['MRData']['RaceTable']['Races'][0]['QualifyingResults'][i]['Q2']
                q2_secs = total_seconds(q2_text)
            except KeyError:
                q2_text = '-'
                q2_secs = '-'

            try:  # Drivers eliminated in Q2 won't be in Q3.
                q3_text = data['MRData']['RaceTable']['Races'][0]['QualifyingResults'][i]['Q3']
                q3_secs = total_seconds(q3_text)

                # Check the driver position. Cannot reference the previous driver if they are position 1.
                if int(data['MRData']['RaceTable']['Races'][0]['QualifyingResults'][i]['position']) > 1:
                    # Subtract the faster driver's time from the current driver to find the delta.
                    q3_delta = round(q3_secs - total_seconds(data['MRData']['RaceTable']['Races'][0]['QualifyingResults'][i-1]['Q3']), 4)
                else:
                    q3_delta = ''

            except KeyError:
                q3_text = '-'
                q3_secs = '-'
                q3_delta = ''

            driver_qualifying = {'fn': fn, 'ln': ln, 'url': url, 'pos': pos,
                                 'q1': {'text': q1_text, 'seconds': q1_secs},
                                 'q2': {'text': q2_text, 'seconds': q2_secs},
                                 'q3': {'text': q3_text, 'seconds': q3_secs, 'delta': q3_delta}}
            driver_list.append(driver_qualifying)

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
