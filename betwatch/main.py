import requests
import pendulum
import json
from fake_useragent import UserAgent
import time
from datetime import datetime

def odd_file():
    with open("logs.txt", "w") as file:
        file.write('\n')

def market_locator():
    ua = UserAgent()
    today = pendulum.today('Europe/Moscow').format('YYYY-MM-DD')
    url = f'https://betwatch.fr/getMoneyway?choice=Match%20Odds&date={today}&live_only=false&prematch_only=false&not_countries=&not_leagues=&settings_order=score&country=&league=&min_vol=0&max_vol=103&min_percent=0&max_percent=100&min_odd=0&max_odd=349&filtering=false&utc=3&step=100'
    # url = f'https://betwatch.fr/getMoneyway?choice=&date={today}&live_only=false&prematch_only=false&not_countries=&not_leagues=&settings_order=score&country=&league=&min_vol=55&max_vol=103&min_percent=75&max_percent=100&min_odd=0&max_odd=349&filtering=true&utc=3&step=100'
    responce = requests.get(
        url=url,
        headers={'user-agent': f'{ua.random}'}
    )

    data = responce.json()
    # print(data)

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    with open('data.json') as json_file:
        src = json.load(json_file)
    # print(src)

    siroe = src['data']
    # print(siroe)
    # with open("logs.txt", "w") as file:
    #     file.write('\n')
    # link_live = ''
    for i in siroe:
        home_team = (i['m'].split('-'))[0]
        # print(home_team)
        away_team = (i['m'].split('-'))[1].lstrip(' ')
        # print(away_team)
        odds_team = i['i']
        # print(odds_team)
        odds_home_team = odds_team[0][2]
        odds_draw_team = odds_team[1][2]
        odds_away_team = odds_team[2][2]
        # print(odds_home_team)
        # print(odds_draw_team)
        # print(odds_away_team)
        market_name = i['n']
        # print(market_name) # Match Odds, Over/Under 0.5 Goals, Both teams to Score?, Half Time, First Half Goals 0.5
        indikator_live = i['l']
        # print(indikator_live)
        market_volume = i['v']
        # print(market_volume)
        sredniy_market_volume = i['vm']
        # print(sredniy_market_volume)
        # print(i['i'])
        id_market = i['e']
        # print(id_market)

        if len(i['i']) == 3:
            team1_volume = i['i'][0][1]
            # print(team1_volume)
            teamx_volume = i['i'][1][1]
            # print(teamx_volume)
            team2_volume = i['i'][2][1]
            # print(team2_volume)

        # elif len(i['i']) == 2:
        #     teamU_volume = i['i'][0][1]
        #     # print(teamU_volume)
        #     teamO_volume = i['i'][1][1]
        #     # print(teamO_volume)
        # if indikator_live == 0:
        #     if market_name == 'Half Time':
        #         print(home_team)
        #         with open("p1.txt", "a") as file:
        #             file.write(home_team + '\n')
        #     if market_name == 'First Half Goals 1.5' and teamO_volume > teamU_volume:
        #         print(home_team)
        #         with open("p1.txt", "a") as file:
        #             file.write(home_team + '\n')

        if indikator_live == 1 and market_volume > 50000:
            link_live = 'https://betwatch.fr/live?live=' + str(id_market)
            # print(link_live)

            au = UserAgent()

            urle = link_live
            responce = requests.get(
                url=urle,
                headers={'user-agent': f'{au.random}'}
            )

            datas = responce.json()

            time_market = datas[f'{id_market}'][0]
            # print(time_market)
            score_market = datas[f'{id_market}'][1]
            # print(score_market)
            current_datetime = datetime.now()
            # print(odds_draw_team)
            if time_market == 'HT' and score_market == '0-0':
                print(current_datetime, id_market, time_market, score_market, home_team, 'X', away_team, market_volume, team1_volume, teamx_volume, team2_volume, odds_home_team, odds_draw_team, odds_away_team)
                with open("logs.txt", "a") as file:
                    file.write(f"{current_datetime}" + '\t' + f"{id_market}" + '\t' + f"{time_market}" + '\t' + f"{score_market}" + '\t' + f"{home_team}" + '\t' + 'X' + '\t' + f"{away_team}" + '\t' + f"{market_volume}" + '\t' + f"{team1_volume}" + '\t' + f"{teamx_volume}" + '\t' + f"{team2_volume}" + '\t' + f"{odds_home_team}" + '\t' + f"{odds_draw_team}" + '\t' + f"{odds_away_team}" + '\n')

def main():
    market_locator()


if __name__ == "__main__":
    odd_file()
    while True:
        # print(f'Last update: {datetime.now()}')
        main()
        time.sleep(15)
