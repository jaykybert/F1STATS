import requests
import json


def current_driver_standings():
    """ Get the current Formula 1 Driver Standings.

    :return driver_dict: A dict containing a sorted list of drivers by points and round info.
    """
    url = 'http://ergast.com/api/f1/current/driverStandings.json'
    response = requests.get(url)
    if not response.ok:
        return []

    data = json.loads(response.text)

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


def current_constructor_standings():
    """ Get the current Formula 1 Constructor Standngs

    :return cons_dict: A dict containing a sorted list of constructors by points and round info.
    """
    url = 'http://ergast.com/api/f1/current/constructorStandings.json'

    response = requests.get(url)
    if not response.ok:
        return []

    data = json.loads(response.text)

    cons_list = []
    for con in data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']:
        name = con['Constructor']['name']
        nation = con['Constructor']['nationality']
        url = con['Constructor']['url']
        points = con['points']
        pos = con['position']
        wins = con['wins']

        con_info = {'name': name, 'nationality': nation, 'url': url,
                    'points': points, 'pos': pos, 'wins': wins}
        cons_list.append(con_info)
            
    cons_dict = {'Constructor': cons_list}

    round_no = data['MRData']['StandingsTable']['StandingsLists'][0]['round']
    season = data['MRData']['StandingsTable']['StandingsLists'][0]['season']
    cons_dict['RoundInfo'] = {'round': round_no, 'season': season}

    return cons_dict
