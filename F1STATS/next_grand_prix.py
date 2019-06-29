import requests
import json
from utils import *


def next_race_info():
    """ Get information for the upcoming Formula 1 race.

    :return: A dict containing information about the next race.
    """
    url = 'http://ergast.com/api/f1/current/next.json'

    response = requests.get(url)
    if not response.ok:
        return []

    data = json.loads(response.text)

    round_n = data['MRData']['RaceTable']['round']
    season = data['MRData']['RaceTable']['season']
    date = date_format(data['MRData']['RaceTable']['Races'][0]['date'])
    country = data['MRData']['RaceTable']['Races'][0]['Circuit']['Location']['country']
    locality = data['MRData']['RaceTable']['Races'][0]['Circuit']['Location']['locality']
    race = data['MRData']['RaceTable']['Races'][0]['raceName']
    circuit = data['MRData']['RaceTable']['Races'][0]['Circuit']['circuitName']
    circuit_url = data['MRData']['RaceTable']['Races'][0]['Circuit']['url']

    return {'country': country, 'locality': locality, 'race': race, 'circuit': circuit, 'url': circuit_url,
            'round': round_n, 'season': season, 'date': date}
