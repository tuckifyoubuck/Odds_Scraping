from draftkings_class import DraftKings

dk_nba = DraftKings(league = "NBA")
dk_nba_games = dk_nba.get_pregame_odds()
dk_nba_game_ids = dk_nba.get_event_ids()

# Obtain list of NBA games and their game IDs
# Obtain pregame markets for each game and outcome for each market and save data to dictionary
# Parse and print dictionary
print('NBA games')
for key, value in dk_nba_game_ids.items():
    print(key + ':', value)

print()

games_nba = dk_nba.get_pregame_odds()
for game in games_nba:
    print(game['game'])
    for market in game['markets']:
        print('\t' + market['marketName'])
        for outcome in market['outcomes']:
            print('\t\t' + outcome['label'] + ':', outcome['odds'])

#print('\n'*10)

#dk.live_odds_stream(
#    event_ids=["28442732", "28443578"], markets=['Moneyline'])