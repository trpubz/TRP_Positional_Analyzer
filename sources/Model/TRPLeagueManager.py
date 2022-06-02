# TRPLeagueManager handles the instantiation of pd.DataFrames

import pandas as pd


class TRPLeagueManager:
    bats = ["OF", "1B", "3B", "2B", "SS", "DH", "C"]  # these strings represent the offensive positions
    arms = ["SP", "RP"]  # these strings represent the pitching positions

    def __init__(self):
        self.hitters: pd.DataFrame = pd.read_json("resources/TRPHitterCards.json"). \
            drop(["idESPN", "idFangraphs", "idSavant"], axis=1)  # drop referential ID keys
        # reorder columns for readability
        self.hitters.reindex(columns=["_name", "tm", "pos", "fantasyTeam",
                                      "wRAA", "wOBA", "xwOBA",
                                      "AB", "PA", "R", "HR", "RBI", "SBN", "OBP", "SLG", "xSLG"])
        self.pitchers: pd.DataFrame = pd.read_json("resources/TRPPitcherCards.json"). \
            drop(["idESPN", "idFangraphs", "idSavant"], axis=1)
        self.pitchers.reindex(columns=["_name", "tm", "pos", "fantasyTeam",
                                       "xERA", "FIP", "wFIP", \
                                       "IP", "QS", "SVHD", "K/9", "ERA", "WHIP"])
