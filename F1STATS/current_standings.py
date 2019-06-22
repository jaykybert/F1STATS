import requests
import json


"""Consider an additional information button?
Gives number of wins, driver numbers, etc.

Link URLS
WRITE DATA AS OF ROUND X, PLACE NAME.
SPLIT THE STANDINGS INTO THEIR OWN PAGES. ADD A HOME PAGE.
"""


def current_driver_standings():
    url = 'http://ergast.com/api/f1/current/driverStandings.json'
    response = requests.get(url)
    if not response.ok:
        return []
    else:
        data = json.loads(response.text)

        standings_list = []
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
            
        standings_list.append(driver_list)
        round_n = data['MRData']['StandingsTable']['StandingsLists'][0]['round']
        season = data['MRData']['StandingsTable']['StandingsLists'][0]['season']
        standings_list.append({'round': round_n, 'season': season})
        
        return standings_list


def current_constructor_standings():
    url = 'http://ergast.com/api/f1/current/constructorStandings.json'

    response = requests.get(url)
    if not response.ok:
        return []
    else:
        data = json.loads(response.text)

        standings_list = []
        con_list = []
        for con in data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']:
            name = con['Constructor']['name']
            nation = con['Constructor']['nationality']
            url = con['Constructor']['url']

            points = con['points']
            pos = con['position']
            wins = con['wins']

            con_info = {'name': name, 'nationality': nation, 'url': url,
                        'points': points, 'pos': pos, 'wins': wins}
            con_list.append(con_info)
            
        standings_list.append(con_list)
        round_no = data['MRData']['StandingsTable']['StandingsLists'][0]['round']
        season = data['MRData']['StandingsTable']['StandingsLists'][0]['season']
        standings_list.append({'round': round_no, 'season': season})

        return standings_list
