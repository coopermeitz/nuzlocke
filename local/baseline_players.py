import numpy as np

from poke_env.player.player import Player
from poke_env.data import TYPE_CHART


class HitHardOrSwitchPlayer(Player):
    """_summary_

    :param Player: _description_
    :type Player: _type_
    """

    def __init__(self, baseline=75, **kwargs):
        """Constructor for the agent.

        :param baseline: The baseline strength that a move should reach in order to be considered, defaults to 75
        :type baseline: int, optional
        """
        super().__init__(**kwargs)
        self.baseline = baseline

    def choose_move(self, battle):
        """Chooses a move to make in the current battle. First, it
        determines finds the strongest effective move (based on accuracy
        and type checks). If the power of that move is above the baseline,
        it attacks using that move. Otherwise, it switches out to a random
        Pokemon. If there is no valid switch, a random move is chosen.

        :param battle: Object representing the state of the current battle.
        :type battle: AbstractBattle
        :return: The move that the player should make in the given situation.
        :rtype: BattleOrder
        """
        # Use type map and accuracy to find the strongest move.
        really_good_move = None
        for move in battle.available_moves:
            type_multiplier = 1
            x = battle.opponent_active_pokemon
            # Iterate through the defending Pokemon's types to get the
            # effectiveness multiplier of the move.
            for t in x.types:
                if t:
                    type_multiplier *= TYPE_CHART[move.type.name][t.name]
            effective_base_dmg = move.base_power * type_multiplier * move.accuracy
            if really_good_move:
                if effective_base_dmg > really_good_move[1]:
                    really_good_move = (move, effective_base_dmg)
            else:
                really_good_move = (move, effective_base_dmg)
        # If no moves reach the required baseline, switch to a random Pokemon.
        if really_good_move and really_good_move[1] >= self.baseline:
            return self.create_order(really_good_move[0])
        else:
            if battle.available_switches:
                return self.create_order(np.random.choice(battle.available_switches))
            else:
                # There are no available switches, so pick a random move.
                return self.choose_random_move(battle)
