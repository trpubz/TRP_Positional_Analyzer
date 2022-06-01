# TRP_Positional_Analyzer
# main.py
# This script runs the module
# by pubins.taylor
# v0.5 - 1 JUN 2022

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# instantiate the global objects
bats = ["OF", "1B", "3B", "2B", "SS", "DH", "C"]  # these strings represent the offensive positions
arms = ["SP", "RP"]  # these strings represent the pitching positions
hitters = pd.read_json("resources/TRPHitterCards.json"). \
    drop(["idESPN", "idFangraphs", "idSavant"], axis=1)  # drop referential ID keys
# reorder columns for readability
hitters = hitters.reindex(columns=["_name", "tm", "pos", "fantasyTeam",
                                   "wRAA", "wOBA", "xwOBA",
                                   "AB", "PA", "R", "HR", "RBI", "SBN", "OBP", "SLG", "xSLG"])
pitchers = pd.read_json("resources/TRPPitcherCards.json"). \
    drop(["idESPN", "idFangraphs", "idSavant"], axis=1)
pitchers = pitchers.reindex(columns=["_name", "tm", "pos", "fantasyTeam",
                                     "xERA", "FIP", "wFIP", \
                                     "IP", "QS", "SVHD", "K/9", "ERA", "WHIP"])


def TRPFilterPosGroup(pos: str):
    if pos.__contains__("P"):
        posPlayers = pitchers[pitchers["pos"].str.contains(pos)]
    else:
        posPlayers = hitters[hitters["pos"].str.contains(pos)]

    print(f"POS: {pos}")
    print(posPlayers.to_string())


if __name__ == '__main__':
    for player in bats:
        TRPFilterPosGroup(pos=player)

    for player in arms:
        TRPFilterPosGroup(pos=player)
