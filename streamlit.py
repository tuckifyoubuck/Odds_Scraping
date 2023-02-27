import streamlit as st
import numpy as np
import pandas as pd
import json
from draftkings_class import DraftKings
from barstool_class import Barstool


# Get NBA odds from DraftKings and save to json
dk_nba = DraftKings(league = "NBA")
dk_nba_df = dk_nba.get_pregame_odds_df()
dk_nba_df = dk_nba_df.astype({'odds':'int'})
dk_nba_df['marketName'] = pd.np.where(dk_nba_df.marketName.str.contains("Money"), "Moneyline",
                          pd.np.where(dk_nba_df.marketName.str.contains("Spread"), "Point Spread",
                          pd.np.where(dk_nba_df.marketName.str.contains("Total"), "Total Points", "THIS IS A BUG")))
dk_nba_df = dk_nba_df.rename({'odds':'odds_dk'}, axis='columns')


# Get NBA odds from Barstool and save to json
bs_nba = Barstool(league = 'NBA')
bs_nba_df = bs_nba.get_pregame_odds_df()
bs_nba_df = bs_nba_df.astype({'odds':'int'})
bs_nba_df['offerName'] = pd.np.where(bs_nba_df.offerName.str.contains("Money"), "Moneyline",
                            pd.np.where(bs_nba_df.offerName.str.contains("Spread"), "Point Spread",
                                pd.np.where(bs_nba_df.offerName.str.contains("Total"), "Total Points", "THIS IS A BUG")))
bs_nba_df = bs_nba_df.rename({'offerName':'marketName', 'odds':'odds_bs'}, axis='columns')


new_df = pd.merge(dk_nba_df, bs_nba_df,  how='inner', left_on = ['game','marketName', 'label'], right_on = ['game','marketName', 'label'])
new_df['bestOdds'] = np.where(new_df['odds_dk'] > new_df['odds_bs'], 'DK',
                    np.where(new_df['odds_bs'] > new_df['odds_dk'], 'BS', 'EVEN'))


# Streamlit dashboard
#st.write('TESTING')
#st.write('DRAFTKINGS')
#st.write(dk_nba_df)
#st.write('BARSTOOL')
#st.write(bs_nba_df)
st.write(new_df)