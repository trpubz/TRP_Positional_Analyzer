# Player File houses the Player abstract class and the Hitter/Pitcher subclass
# by pubins.taylor
# v0.3
# created 22 MAY 2022
# TODO: add player stats as properties; need to create logic for subclassing hitters/pitchers
# lastUpdate 22 MAY 2022


class Player:

    def __init__(self, espnid, fgid, savid, name, pos, mlbTeam):
        self.idESPN = espnid
        self.idFangraphs = fgid
        self.idSavant = savid
        self.name = name
        self.pos: str = pos
        self.mlbTeam = mlbTeam
        self.curTeam: str = ""

    def __eq__(self, other: tuple[str, str]) -> bool:
        """
        Builtin equality override where a match is performed based on name and MLB team
        :param other: The other player seeking equality based on a tuple containing their name and MLB team
        :return: bool
        """
        if self.name == other[0] and self.mlbTeam == team_map(other[1]):
            return True
        else:
            return False

    def eligiblePos(self) -> list(str):
        return self.pos.split("/")


@staticmethod
def team_map(tm: str) -> str:
    """
    ESPN likes to use weird MLB Team abbreviations.  This reference function aligns MLB abbreviations with TRPKeys.
    :param tm: the player's MLB tm that EPSN uses on the Draft Recap page
    :return: the corrected string in-line with TRPKeys
    """
    if tm == "CHW":
        return "CWS"
    elif tm == "KCR":
        return "KC"
    elif tm == "SDP":
        return "SD"
    elif tm == "SFG":
        return "SF"
    elif tm == "WSN":
        return "WSH"
    else:
        return tm

