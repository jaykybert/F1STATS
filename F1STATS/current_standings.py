import requests
import json

import pprint


def current_driver_standings(round_no=None, season=None):
    """ Get the current Formula 1 Driver Standings.
    :param round_no: Round of standings.
    :param season: Season of standings.
    :return driver_dict: A dict containing a sorted list of drivers by points and round info.
    """
    if round_no is None:
        if season is None:  # Final standings, current season.
            url = 'https://ergast.com/api/f1/current/driverStandings.json'
        else:  # Final standings, specific season.
            url = 'https://ergast.com/api/f1/{}/driverStandings.json'.format(season)
    else:
        if season is None:  # Specific round standings, current season.
            url = 'https://ergast.com/api/f1/current/{}/driverStandings.json'.format(round_no)
        else:  # Specific round standings, specific season.
            url = 'https://ergast.com/api/f1/{}/{}/driverStandings.json'.format(season, round_no)

    response = requests.get(url)
    if not response.ok:
        return []

    try:
        data = json.loads(response.text)
        # Some invalid requests pass .ok but with an empty data structure.
        if len(data['MRData']['StandingsTable']['StandingsLists']) == 0:
            return []

        driver_list = []
        for driver in data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']:
            fn = driver['Driver']['givenName']
            ln = driver['Driver']['familyName']
            nation = driver['Driver']['nationality']
            url = driver['Driver']['url']
            cons = driver['Constructors'][0]['name']
            points = driver['points']
            pos = driver['position']
            wins = driver['wins']

            driver_info = {'fn': fn, 'ln': ln, 'url': url, 'points': points,
                           'pos': pos, 'wins': wins, 'nationality': nation,
                           'cons': cons}
            driver_list.append(driver_info)

        driver_dict = {'Driver': driver_list}
        round_n = data['MRData']['StandingsTable']['StandingsLists'][0]['round']
        season = data['MRData']['StandingsTable']['StandingsLists'][0]['season']
        driver_dict['RoundInfo'] = {'round': round_n, 'season': season}

        return driver_dict

    except ValueError:
        return []


def current_constructor_standings(round_no=None, season=None):
    """ Get the current Formula 1 Constructor Standings
    :param round_no: Round of standings.
    :param season: Season of standings.
    :return cons_dict: A dict containing a sorted list of constructors by points and round info.
    """
    if round_no is None:
        if season is None:  # Final standings, current season.
            url = 'https://ergast.com/api/f1/current/constructorStandings.json'
        else:  # Final standings, specific season.
            url = 'https://ergast.com/api/f1/{}/constructorStandings.json'.format(season)
    else:
        if season is None:  # Specific round standings, current season.
            url = 'https://ergast.com/api/f1/current/{}/constructorStandings.json'.format(round_no)
        else:  # Specific round standings, specific season.
            url = 'https://ergast.com/api/f1/{}/{}/constructorStandings.json'.format(season, round_no)

    response = requests.get(url)
    if not response.ok:
        return []

    try:
        data = json.loads(response.text)
        # Some invalid requests pass .ok but with an empty data structure.
        if len(data['MRData']['StandingsTable']['StandingsLists']) == 0:
            return []

        cons_dict = {}
        round_no = data['MRData']['StandingsTable']['StandingsLists'][0]['round']
        season = data['MRData']['StandingsTable']['StandingsLists'][0]['season']
        cons_dict['RoundInfo'] = {'round': round_no, 'season': season}

        cons_list = []
        for con in data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']:
            name = con['Constructor']['name']
            nation = con['Constructor']['nationality']
            url = con['Constructor']['url']
            points = con['points']
            pos = con['position']
            wins = con['wins']
            win_percent = round((int(wins) / int(round_no)) * 100, 1)

            con_info = {'name': name, 'nationality': nation, 'url': url,
                        'points': points, 'pos': pos, 'wins': {'number': wins, 'percentage': win_percent}}
            cons_list.append(con_info)

        cons_dict['Constructor'] = cons_list

        return cons_dict

    except ValueError:
        return []
