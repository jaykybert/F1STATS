import requests
import json


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

        for i in range(len(data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings'])):
            fn = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings'][i]['Driver']['givenName']
            ln = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings'][i]['Driver']['familyName']
            nation = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings'][i]['Driver']['nationality']
            url = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings'][i]['Driver']['url']
            cons = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings'][i]['Constructors'][0]['name']
            pos = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings'][i]['position']
            wins = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings'][i]['wins']
            points = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings'][i]['points']

            if int(pos) > 1:  # Cannot refer to a driver above P1.
                points_delta = int(points) - int(data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings'][i-1]['points'])
            else:
                points_delta = ''

            driver_info = {'fn': fn, 'ln': ln, 'url': url, 'points': points, 'delta': points_delta,
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
        round_n = data['MRData']['StandingsTable']['StandingsLists'][0]['round']
        season = data['MRData']['StandingsTable']['StandingsLists'][0]['season']
        cons_dict['RoundInfo'] = {'round': round_n, 'season': season}

        cons_list = []

        for i in range(len(data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings'])):
            name = data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings'][i]['Constructor']['name']
            nation = data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings'][i]['Constructor']['nationality']
            url = data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings'][i]['Constructor']['url']
            pos = data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings'][i]['position']
            wins = data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings'][i]['wins']
            win_percent = round((int(wins) / int(round_n)) * 100, 1)
            points = data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings'][i]['points']

            if int(pos) > 1:
                points_delta = int(points) - int(data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings'][i-1]['points'])
            else:
                points_delta = ''

            con_info = {'name': name, 'nationality': nation, 'url': url, 'points': points, 'delta': points_delta,
                        'pos': pos, 'wins': {'number': wins, 'percentage': win_percent}}
            cons_list.append(con_info)

        cons_dict['Constructor'] = cons_list

        return cons_dict

    except ValueError:
        return []
