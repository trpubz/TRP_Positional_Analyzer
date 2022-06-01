# TRP_Positional_Analyzer
# main.py
# This script runs the module
# by pubins.taylor
# v0.1 - 30 MAY 2022

import pandas as pd
import matplotlib

bats = ["OF", "1B", "3B", "2B", "SS", "DH", "C"]
arms = ["SP", "RP"]
hitters = pd.read_json("resources/TRPHitterCards.json")
pitchers = pd.read_json("resources/TRPPitcherCards.json")

def TRPFilterHitters(pos: str):
    posPlayers = hitters[hitters["pos"].str.contains(pos)]
    print(f"POS: {pos}")
    print(posPlayers)


if __name__ == '__main__':
    for p in bats:
        TRPFilterHitters(pos=p)


