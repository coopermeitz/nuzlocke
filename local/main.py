import asyncio
from tabulate import tabulate

# poke_env imports. LocalhostServerConfiguration needed to connect to Showdown running locally.
# See poke_env docs for details on how to set this up.
from poke_env.server_configuration import LocalhostServerConfiguration
from poke_env.player.random_player import RandomPlayer
from poke_env.teambuilder.constant_teambuilder import ConstantTeambuilder
from poke_env.player.utils import cross_evaluate


import cooper
from baseline_players import HitHardOrSwitchPlayer
from constant_teams import TEAM_1, TEAM_2, TEAM_3


async def main():
    # Add my agent to the list of players.
    players = [cooper.cooper_player]
    # Initialize players to test the main agent against.
    teams = [TEAM_1, TEAM_2, TEAM_3]
    for t in teams:
        players.append(RandomPlayer(
            battle_format="gen8nationaldexag",
            team=ConstantTeambuilder(t),
            max_concurrent_battles=10,
        ))
        players.append(HitHardOrSwitchPlayer(
            battle_format="gen8nationaldexag",
            team=ConstantTeambuilder(t),
            max_concurrent_battles=10,
        ))

    # Evaluate all players with provided utility functions. Copied from docs.
    cross_evaluation = await cross_evaluate(players, n_challenges=100)
    table = [["-"] + [p.username for p in players]]

    # Adds one line per player with corresponding results
    for p_1, results in cross_evaluation.items():
        table.append([p_1] + [cross_evaluation[p_1][p_2] for p_2 in results])

    # Displays results in a nicely formatted table.
    print(tabulate(table))

if __name__ == "__main__":
    # server command:
    # node pokemon-showdown start --no-security
    asyncio.get_event_loop().run_until_complete(main())
