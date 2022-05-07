import numpy as np

from poke_env.player.player import Player
from poke_env.teambuilder.constant_teambuilder import ConstantTeambuilder
# from poke_env.player_configuration import PlayerConfiguration
from poke_env.data import TYPE_CHART
TEAM_STR = """
Hitmontop (M) @ Life Orb  
Ability: Intimidate  
EVs: 252 Atk / 4 SpD / 252 Spe  
Jolly Nature  
- Fake Out  
- Close Combat  
- Mach Punch  
- Rapid Spin  

Mamoswine @ Choice Band  
Ability: Thick Fat  
EVs: 252 Atk / 4 Def / 252 Spe  
Adamant Nature  
- Icicle Crash  
- Earthquake  
- Ice Shard  
- Knock Off  

Gyarados @ Lum Berry  
Ability: Moxie  
EVs: 252 Atk / 4 SpD / 252 Spe  
Adamant Nature  
- Dragon Dance  
- Waterfall  
- Ice Fang  
- Power Whip  

Ambipom @ Sitrus Berry  
Ability: Technician  
EVs: 252 Atk / 4 SpD / 252 Spe  
Adamant Nature  
- Brick Break  
- Fake Out  
- U-turn  
- Agility  

Alakazam @ Focus Sash  
Ability: Magic Guard  
EVs: 252 SpA / 4 SpD / 252 Spe  
Timid Nature  
- Nasty Plot  
- Psychic  
- Focus Blast  
- Shadow Ball  

Raikou @ Heavy-Duty Boots  
Ability: Inner Focus  
EVs: 252 SpA / 4 SpD / 252 Spe  
Timid Nature  
- Volt Switch  
- Thunderbolt  
- Scald  
- Toxic  

"""


# cooper_config = PlayerConfiguration("cooper", None)


class Cooper(Player):
    def choose_move(self, battle):
        """Chooses the best possible move based on AI.
        For now, it is identical to the HitHardOrSwitch agent.

        :param battle: Object representing the state of the current battle.
        :type battle: AbstractBattle
        :return: The move that the player should make in the given situation.
        :rtype: BattleOrder
        """
        # Use typing to find strongest move.
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
        # If none are net base power over 75, switch randomly
        if really_good_move and really_good_move[1] >= 75:
            return self.create_order(really_good_move[0])
        else:
            if battle.available_switches:
                return self.create_order(np.random.choice(battle.available_switches))
            else:
                return self.choose_random_move(battle)


cooper_player = Cooper(battle_format="gen8nationaldexag",
                       team=ConstantTeambuilder(TEAM_STR), max_concurrent_battles=10)
