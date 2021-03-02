from datetime import datetime

def main():
    pass

class base(object):
    """A class to store data on PUBG matches and cheaters"""

    def __init__(self):
        """Creates an empty base"""
        self.objects = {}

    def add_obj(self, obj):
        """Adds an object (cheater or match) to a base
        if it is not already there"""
        if obj not in self.objects:
            self.objects[obj] = []

    def get_obj_info(self, obj):
        """Returns object's (cheater or match) information
        (time cheater started cheating/banned and kills in match)"""
        return self.objects[obj]

class kills_base(base):
    """A class to store data on kills in PUBG matches"""

    def add_kill_info(self, match, info):
        """Adds a kill took place at a certain match.
        Takes the id of match and the kill to add"""
        self.objects[match].append(info)

    def get_matches(self):
        """Returns a list of avaliable matches in the base"""
        return list(self.objects.keys())

    def get_killers_in_match(self, match):
        """Takes match id and returns a list of killers in this match"""
        return [kill[0] for kill in self.get_obj_info(match)]

    def get_killed_in_match(self, match):
        """Takes match id and returns the list of killed players in this match"""
        return [kill[1] for kill in self.get_obj_info(match)]

    def get_kills_times(self, player_id, match):
        """Takes player's and match's id.
        Returns the sorted list of kills times by the player in the match."""
        return sorted([kill[2] for kill in self.get_obj_info(match) if kill[0] == player_id])

    def get_player_victims(self, player_id, match):
        """Takes player's and match's id.
        Returns the players killed and killtimes by the player in the match."""
        return [kill[1:3] for kill in self.get_obj_info(match) if kill[0] == player_id]

    def get_cheaters_in_match(self, match, cheaters):
        """Takes match ID and a base of cheaters.
        Returns list of cheaters in the match."""

        # Searching the time of the first kill in the match
        first_k = min([kill[2] for kill in self.get_obj_info(match)])

        cheat_list = cheaters.get_cheaters()

        killers = self.get_killers_in_match(match)

        # List contains only those started chaeting before the match
        cheaters_in_match = [c for c in cheat_list if cheaters.get_obj_info(c)[0] < first_k and c in killers]

        # Returns the list of cheaters in the match
        return list(set(cheaters_in_match))

class cheaters_base(base):
    """A class to store data on cheaters in PUBG matches"""

    def add_cheater_info(self, obj, info):
        """Takes an id of cheater and adds information on them"""
        self.objects[obj].extend(info)

    def get_cheaters(self):
        """Returns the list of cheaters' id's in a cheaters base"""
        return list(self.objects.keys())

    def get_started_cheating(self, player_id):
        """Takes cheater id and returns date and time they started cheating"""
        return self.get_obj_info(player_id)[0]


def extract_kills(file):
    """Creates the instance of class kills_base()
    and fills with data from a .txt file."""

    kills = kills_base()

    for line in open(file, 'r'):

        kill = line.strip().split('\t')

        # Changes date in text format to datetime format
        kill[3] = datetime.fromisoformat(kill[3])

        # Adds kills to a match
        kills.add_obj(kill[0])
        kills.add_kill_info(kill[0], kill[1:4])

    return kills

def extract_cheaters(file):
    """Creates the instance of class cheaters_base()
    and fills with data from the .txt file."""

    cheaters = cheaters_base()

    for line in open(file, 'r'):

        cheater = line.strip().split('\t')

        # Changes date in text format to datetime format
        cheater[1] = datetime.fromisoformat(str(cheater[1] + ' 00:00'))
        cheater[2] = datetime.fromisoformat(str(cheater[2] + ' 00:00'))

        # Adds infromation on cheaters
        cheaters.add_obj(cheater[0])
        cheaters.add_cheater_info(cheater[0], cheater[1:3])

    return cheaters

if __name__ == '__main__':
    main()
