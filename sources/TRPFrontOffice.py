# Team Model -- The Front Office is where the model and logic resides for the Fantasy Team.
# by pubins.taylor
# v0.2
# created 20 APR 2022
# refactored for generic roster placement
# TODO: create mapping function to sum all player stats in self.roster property
# lastUpdate 26 APR 2022

import TRPPlayer


class Team:

    def __init__(self, abbrv, name, owner):
        self.abbrv = abbrv
        self.name = name
        self.owner = owner
        self.roster: {str: TRPPlayer} = {}

    def add_player(self, plyr: TRPPlayer):
        """
        Adds player to the self roster object
        :param plyr: Player object
        :return n/a
        """
        if "P" in plyr.pos:
            if "SP" in plyr.pos:
                for i in range(3):
                    if self.roster.get("SP" + str(i + 1)) is None:
                        self.roster["SP" + str(i + 1)] = plyr
                        print(f"{self.name} rostered {plyr.name} at SP{i + 1}")
                        return
                # The P roster spot can be rostered by an SP or RP
                for i in range(2):
                    if self.roster.get("P" + str(i + 1)) is None:
                        self.roster["P" + str(i + 1)] = plyr
                        print(f"{self.name} rostered {plyr.name} at P{i + 1}")
                        return
                if self.roster.get("P2") is not None:
                    self.bench_guy(plyr)
            elif "RP" in plyr.pos:
                for i in range(2):
                    if self.roster.get("RP" + str(i + 1)) is None:
                        self.roster["RP" + str(i + 1)] = plyr
                        print(f"{self.name} rostered {plyr.name} at RP{i + 1}")
                        return
                # The P roster spot can be rostered by an SP or RP
                for i in range(2):
                    if self.roster.get("P" + str(i + 1)) is None:
                        self.roster["P" + str(i + 1)] = plyr
                        print(f"{self.name} rostered {plyr.name} at P{i + 1}")
                        return
                if self.roster.get("P2") is not None:
                    self.bench_guy(plyr)
        else:  # Hitters
            for i in range(9):
                if self.roster.get("BAT" + str(i + 1)) is None:
                    self.roster["BAT" + str(i + 1)] = plyr
                    print(f"{self.name} rostered {plyr.name} at BAT{i + 1}")
                    return
            if self.roster.get("BAT9") is not None:
                self.bench_guy(plyr)

    def bench_guy(self, plyr: TRPPlayer):
        for i in range(5):
            if self.roster.get("BN" + str(i + 1)) is None:
                self.roster["BN" + str(i + 1)] = plyr
                print(f"{self.name} benched {plyr.name}")
                return
