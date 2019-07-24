import requests
import json
import utils


def race_calendar():
    """ Get information on the current Formula 1 calendar.

    :return race_list: A list of the races this F1 season.
    """
    url = 'http://ergast.com/api/f1/current.json'

    response = requests.get(url)
    if not response.ok:
        return []

    try:
        data = json.loads(response.text)

        race_dict = {'year': data['MRData']['RaceTable']['season']}
        race_list = []
        for race in data['MRData']['RaceTable']['Races']:
            date_text = race['date']
            date_datetime = utils.return_datetime(date_text)
            date_text = utils.date_format(date_text)
            round_n = race['round']
            circuit = race['Circuit']['circuitName']
            circuit_url = race['Circuit']['url']

            locality = race['Circuit']['Location']['locality']
            race = race['raceName']

            race_info = {'round': round_n, 'circuit': circuit, 'url': circuit_url, 'locality': locality, 'race': race,
                         'date': {'text': date_text, 'datetime': date_datetime}}

            race_list.append(race_info)
        race_dict['Races'] = race_list

        return race_dict

    except ValueError:
        return []
