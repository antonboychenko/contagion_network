from datetime import datetime, timedelta
import random
from bases import *

def main():
    pass

def find_observers(kills, cheaters):
    """Returns the list of players observed cheating behavior.
    Takes data on kills in multiple games of class kills_base()
    and data on cheaters of class cheaters_base()."""

    players_obs_cheating = []

    # Iterates thorugh all matches
    for match in kills.get_matches():

        # Extracts all cheaters in this match
        cheaters_in_match = kills.get_cheaters_in_match(match, cheaters)

        # Finds observers only if there are cheaters in match
        if cheaters_in_match != []:

            # Finds all killers in match
            killers = kills.get_killers_in_match(match)
            # Dummy time far in the future to find the earliest cheater third kill
            min_third_kill = datetime(3000,1,1)

            # Assuming more than one cheater in a match
            for cheater in cheaters_in_match:
                # Finds players killed by cheaters and adds to the final list
                killed_by_cheater = kills.get_player_victims(cheater, match)
                players_obs_cheating.extend(killed_by_cheater)

                # If cheater kills 3 or more times takes the time of its 3rd kill
                if killers.count(cheater) >= 3:
                    third_kill = kills.get_kills_times(cheater, match)[2]

                    # Finds the earliest 3rd kill by cheater
                    if third_kill < min_third_kill:
                        min_third_kill = third_kill

            # Adds all players killed after the earliest 3rd kill by a cheater
            players_obs = [kill[1:3] for kill in kills.get_obj_info(match) if kill[2] > min_third_kill]
            players_obs_cheating.extend(players_obs)

            # In case cheater kills more than 3 times adds match winners
            if min_third_kill != datetime(3000,1,1):
                killed = kills.get_killed_in_match(match)
                # Adding winners using a timestamp of the third kill
                winners = [[player, min_third_kill] for player in killers if player not in killed]
                players_obs_cheating.extend(winners)

    # The method to find the unique observations found on Stackoverflow. Reference below
    players_obs_cheating = [list(x) for x in set(tuple(x) for x in players_obs_cheating)]

    return players_obs_cheating

def find_motifs(players_obs_cheating, cheaters):
    """Takes the list of players observed cheating with time of 'death'.
    Returns the list of players who became cheaters in least than 5 days."""
    motifs = []

    # Extracts all cheaters
    cheat_list = cheaters.get_cheaters()

    # Checks for each observer whether they became cheater within 5 days
    for player in players_obs_cheating:

        if player[0] in cheat_list and\
        timedelta(days = 0) < (cheaters.get_started_cheating(player[0]) - player[1]) <= timedelta(days = 5):

            motifs.append(player[0])

    return list(set(motifs))

def shuffle_network(kills, cheaters):
    """Shuffles the network in place using node label permutation"""

    for match in kills.get_matches():

        cheaters_in_match = kills.get_cheaters_in_match(match, cheaters)

        all_kills = kills.get_obj_info(match)

        # Creating a list of non-cheating players to shuffle
        kills_no_cheat = [kill[0] for kill in all_kills if kill[0] not in cheaters_in_match]
        death_no_cheat = [kill[1] for kill in all_kills if kill[1] not in cheaters_in_match]
        all_no_cheat = kills_no_cheat + death_no_cheat
        all_no_cheat = list(set(all_no_cheat))


        # Creating a random shuffling rule
        rule = {}
        rule = {i:[] for i in all_no_cheat}
        random.shuffle(all_no_cheat)

        i = 0
        for key in rule.keys():
            rule[key] = all_no_cheat[i]
            i += 1

        # Conducting shuffling replacing each id with another
        for kill in all_kills:

            if kill[0] not in cheaters_in_match:
                kill[0] = rule[kill[0]]
            if kill[1] not in cheaters_in_match:
                kill[1] = rule[kill[1]]


if __name__ == '__main__':
    main()
