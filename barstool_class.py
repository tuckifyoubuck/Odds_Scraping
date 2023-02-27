import requests
import pandas as pd
from traceback import print_exc
import json

id_dict = {
    'NHL': 'ice_hockey/nhl',
    'NBA': 'basketball/nba',
    'MLB': 'baseball/mlb'
}

class Barstool:
    def __init__(self, league='NBA'):
        """
        Initializes a class object

        :league str: Name of the league, NBA by default
        """
        self.league = league
        self.pregame_url = f"https://eu-offering-api.kambicdn.com/offering/v2018/pivuspa/listView/{id_dict['NBA']}/all/all/matches.json?market=US&market=US&includeParticipants=true&useCombined=true&lang=en_US"

    def get_event_ids(self) -> dict:
        """
        Finds all the games & their event_ids for the given league
        :rtype: dict
        """
        event_ids = {}
        response = requests.get(self.pregame_url).json()
        for game in response['events']:
            event_ids[game['event']['name']] = game['event']['id']
        return event_ids

    def get_pregame_odds(self) -> list:
        """
        Collects the market odds for the main markets [the ones listed at the league's main url] for the league
        E.g. for the NHL, those are Puck Line, Total and Moneyline
        Returns a list with one object for each game
        :rtype: list
        """
        # List that will contain dicts [one for each game]
        games_list = []

        # Requests the content from Barstool's API, loops through the different games & collects all the material deemed relevant
        response = requests.get(self.pregame_url).json()
        games = response['events']

        for game in games:
            game_label = game['event']['name']
            game_id = game['event']['id']
            # List that will contain dicts (one for each offer)
            offer_list = []
            for offer in game['betOffers']:
                offer_name = offer['criterion']['label']
                # List that will contain dicts (one for each outcome)
                outcome_list = []
                for outcome in offer['outcomes']:
                    try:
                        outcome_line = str(outcome['line'] / 1000)
                        outcome_label = outcome['label'] + ' ' + outcome_line
                    except:
                        outcome_label = outcome['label']
                    outcome_odds = outcome['oddsAmerican']
                    outcome_list.append(
                        {'label': outcome_label, 'odds': outcome_odds}
                    )
                offer_list.append(
                    {'offerName': offer_name, 'outcomes': outcome_list}
                )
            games_list.append(
                {'game': game_label, 'offers': offer_list}
            )
        return games_list

    def store_as_json(self, games_list, file_path: str = None):
        """
        Dumps the scraped content into a JSON-file in the same directory

        :rtype: None, simply creates the file and prints a confirmation
        """
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(games_list, file)
            print(f"Content successfully dumped into '{file_path}'")
            return file_path
        else:
            with open(self.league.lower() + '_bs.json', 'w') as file:
                json.dump(games_list, file)
            print(f"Content successfully dumped into '{self.league.lower() + '_bs.json'}'")
            return self.league.lower() + '_bs.json'

    def get_pregame_odds_df(self):
        odds = self.get_pregame_odds()
        try:
            df = pd.json_normalize(odds)
            df = df.explode('offers').reset_index(drop=True)
            df = df.merge(pd.json_normalize(df['offers']), left_index=True, right_index=True).drop(['offers'], axis=1)
            df = df.explode('outcomes').reset_index(drop=True)
            df = df.merge(pd.json_normalize(df['outcomes']), left_index=True, right_index=True).drop(['outcomes'], axis=1)
            return df
        except Exception as e:
            print(e)







