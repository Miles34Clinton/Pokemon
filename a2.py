from typing import Counter, Dict, List, Optional, Tuple
from a2_support import *
import math


# Replace these <strings> with your name, student number and email address.
__author__ = "<Boxiang Yang>, <46440266>"
__email__ = "<boxiang.yang@uqconnect.edu.au>"

# Before submission, update this tag to reflect the latest version of the
# that you implemented, as per the blackbaord changelog. 
__version__ = 1.0

# Implement your classes here.
class PokemonStats(object):
    """A class modelling the stats of a pokemon. These stats must be non-negative."""
    def __init__(self, stats: Tuple[float, int, int, int]) -> None:
        """Constructs an instance of PokemonStats.
        
        Parameters:
            stats:(Tuple[float, int, int, int]):The base list of stats to encapsulate. 
                These values can be assumed to be non-negative.
        """
        self._hit_chance = stats[STAT_HIT_CHANCE]
        self._health = stats[STAT_MAX_HEALTH]
        self._attack = stats[STAT_ATTACK]
        self._defense = stats[STAT_DEFENSE]
        
    def level_up(self) -> None:
        """Grows the PokemonStats instance after the pokemon has levelled up."""
        self._hit_chance = 1
        self._health = int(self.get_max_health() * LEVEL_UP_STAT_GROWTH)
        self._attack = int(self.get_attack() * LEVEL_UP_STAT_GROWTH)
        self._defense = int(self.get_defense() * LEVEL_UP_STAT_GROWTH)

    def get_hit_chance(self) -> float:
        """Return the pokemon's current chance at making a successful attack.
        
        Returns:
            (float): The probability of success in every attack.
        """
        return  self._hit_chance

    def get_max_health(self) -> int:
        """Return the pokemon's max health.
        
        Returns:
            (int): Maximum health limit.
        """
        return self._health

    def get_attack(self) -> int:
        """Return the pokemon's attack stat.

        Returns:
            (int): Attack power.
        """
        return self._attack

    def get_defense(self) -> int:
        """Return the pokemon's defense stat.

        Returns:
            (int): Defense value.
        """
        return self._defense

    def apply_modifier(self, modifier: Tuple[float, int, int, int]) -> 'PokemonStats':
        """Applies a stat modifier and returns the newly constructed, modified pokemon stats.
        
        Parameters:
            modifier(Tuple[float, int, int, int]): A list of stat modifications to apply, 
                                                of the same structure as the initial supplied pokemon stats.

        Returns:
            ('PokemonStats'): PokemonStats corresponding to the given name.
        """
        return PokemonStats((
            self._hit_chance + modifier[0] if self._hit_chance + modifier[0] > 0 else 0, 
            self._health + modifier[1] if self._health + modifier[1] > 0 else 0, 
            self._attack + modifier[2] if self._attack + modifier[2] > 0 else 0,
            self._defense + modifier[3] if self._defense + modifier[3] > 0 else 0 
        ))

    def __str__(self) -> str:
        """(str): Returns the string representation of this class."""
        return f'PokemonStats(({self._hit_chance}, {self._health}, {self._attack}, {self._defense}))'

    def __repr__(self) -> str:
        """(repr): Returns the string representation of this class."""
        return f'PokemonStats(({self._hit_chance}, {self._health}, {self._attack}, {self._defense}))'


class Pokemon(object):
    """A class which represents a Pokemon."""
    def __init__(self, name: str, stats: PokemonStats, element_type: str, 
                moves: List['Move'], level: int = 1) -> None:
        """Creates a Pokemon instance.
        
        Parameters:
            name(str): The name of this pokemon.
            stats(PokemonStats): The pokemon's stats.
            element_type(str): The name of the type of this pokemon.
            moves(List['Move']): A list of containing the moves that this pokemon will have learned after it is instantiated.
            level(int): The pokemon's level.
        """    
        self._name = name
        self._stats = stats
        self._health = stats.get_max_health()
        self._element_type = element_type
        self._level = level
        self._experience = self._level ** 3
        self._move_info: List[Tuple['Move', int]] = []
        for move in moves:
            """Iterate over the information for each move in the move list."""
            self._move_info.append((move, move.get_max_uses()))
        self._modification_list = []

    def get_name(self) -> str:
        """Get this pokemon's name.
        
        Returns:
            (str): Get this pokemon's name.
        """
        return self._name
    
    def get_health(self) -> int:
        """Get the remaining health of this pokemon.

        Returns:
            (int): Get the remaining health number of this pokemon.
        """
        return self._health

    def get_max_health(self) -> int:
        """Get the maximum health of this pokemon before stat modifiers are applied.

        Returns:
            (int): Get the maximum health number of this pokemon        
        """
        return self._stats.get_max_health()

    def get_element_type(self) -> str:
        """Get the name of the type of this pokemon.
        
        Returns:
            (str): Get the name of the type of this pokemon.
        """
        return self._element_type

    def get_remaining_move_uses(self, move: 'Move') -> int:
        """Gets the number of moves left for the supplied move, or 0 if the pokemon doesn't know the move.
        
        Parameters:
            move(Move): Move performed by the Pokemon.

        Returns:
            (int):Gets the number of moves left for the supplied move.
        """
        for learned_move in self._move_info:
            """Iterate over the information for each learned move in the move information list."""
            if learned_move[0] == move:
                """Find the move in the move information list that is the same as the input move parameter."""
                return learned_move[1]

    def get_level(self) -> int:
        """Get the level of this pokemon.
        
        Returns:
            (int):Gets the number of level of this pokemon.
        """
        return self._level

    def get_experience(self) -> int:
        """Return the current pokemon's experience.
        
        Returns:
            (int):Gets the number of experience of this pokemon.
        """
        return self._experience

    def get_next_level_experience_requirement(self) -> int:
        """Return the total experience required for the pokemon to be one level higher.
        
        Returns:
            (int):Gets the number of required experience of next level.
        """
        next_level_experience_requirement = (self._level + 1) ** 3
        return next_level_experience_requirement

    def get_move_info(self) -> List[Tuple['Move', int]]:
        """Return a list of the pokemon's known moves and their remaining uses.

        Returns:
            (List): Gets the list of move information.
        """
        return sorted(self._move_info, key=lambda key: key[0].get_name())

    def has_fainted(self) -> bool:
        """Return true if the pokemon has fainted.

        Returns:
            (bool): Identify if the pokemon has fainted.
        """
        if self._health <= 0:
            """Let's say the Pokemon has zero health."""
            return True
        else:
            return False

    def modify_health(self, change: int) -> None:
        """Modify the pokemons health by the supplied amount.
        
        Parameters:
            change(int): The health change to be applied to the pokemon.
        """
        modified_health = self._health + change
        if modified_health >= self.get_stats().get_max_health():
            """Assume that the adjusted Health of the Pokemon is greater than its maximum health."""
            self._health = self.get_stats().get_max_health()
        elif modified_health < 0:
            self._health =  0
        else:
            self._health =  modified_health

    def gain_experience(self, experience: int) -> None:
        """Increase the experience of this pokemon by the supplied amount, and level up if necessary.
        
        Parameters:
            experience(int): The amount of experience points to increase.
        """
        self._experience += experience
        new_level = math.floor(self._experience ** (1/3))
        for _ in range(new_level - self.get_level()):
            """Iterate over how many levels pokemon have advanced in total, and update the upgraded properties."""
            self.level_up()

    def level_up(self) -> None:
        """Increase the level of this pokemon."""
        old_max_health = self._stats.get_max_health()
        self._stats.level_up()
        self._level += 1
        heal = self._stats.get_max_health() - old_max_health
        self._health += heal

    def experience_on_death(self) -> int:
        """The experience awarded to the victorious pokemon if this pokemon faints.
        
        Returns:
            (int): Gained experience from this fainted pokemon.
        """
        return int(200 * self._level / 7)

    def can_learn_move(self, move: 'Move') -> bool:
        """Returns true if the pokemon can learn the given move.
        
        Parameters:
            move('Move'): move for pokemon to learn.

        Returns:
            (bool): Identify if this pokemon can learn this move.
        """
        if len(self._move_info) >= MAXIMUM_MOVE_SLOTS:
            """Assume that the moves in the move list are greater than or equal to the maximum number of move that can be held."""
            return False
        else:
            for learned_move in self._move_info:
                if learned_move[0] == move:
                    return False
                else:
                    pass
            return True

    def learn_move(self, move: 'Move') -> None:
        """Learns the given move, assuming the pokemon is able to.
        
        Parameters:
            move('Move'): move for pokemon to learn.
        """
        self._move_info.append((move, move.get_max_uses()))

    def forget_move(self, move: 'Move') -> None:
        """Forgets the supplied move, if the pokemon knows it.

        Parameters:
            move('Move'): move for pokemon to forget.
        """
        for learned_move in self._move_info:
            """Iterate over each learned move in the move list."""
            if learned_move[0] == move:
                self._move_info.remove(learned_move)

    def has_moves_left(self) -> bool:
        """Returns true if the pokemon has any moves they can use.

        Returns:
            (bool): Identify if this pokemon has remaining move.
        """
        for learned_move in  self._move_info:
            """Iterate over each learned move in the move list."""
            if learned_move[1] > 0:
                return True
            else:
                pass
        return False

    def reduce_move_count(self, move: 'Move') -> None:
        """Reduce the move count of the move if the pokemon has learnt it.

        Parameters:
            move('Move'): move for pokemon to reduce it uses.       
        """
        for learned_move in self._move_info:
            """Iterate over each learned move in the move list."""
            if learned_move[0] == move:
                count = learned_move[1] - 1
                self._move_info.remove(learned_move)
                self._move_info.append((move, count))

    def add_stat_modifier(self, modifier: Tuple[float, int, int, int], rounds: int) -> None:
        """Adds a stat modifier for a supplied number of rounds.
        
        Parameters:
            modifier('Tuple[float, int, int, int]'): A stat modifier to be applied to the pokemon.
            rounds(int): The number of rounds that the stat modifier will be in effect for.         
        """
        self._modification_list.append((modifier, rounds))
        new_stats = self.get_stats()
        new_max_health = new_stats.get_max_health()
        if self._health > new_max_health:
            """Assume that the current health is greater than the updated health upper limit."""
            self._health = new_max_health
        else:
            pass

    def get_stats(self) -> PokemonStats:
        """Return the pokemon stats after applying all current modifications.

        Returns:
            (PokemonStats): Get current pokemon stats.
        """
        new_stats = self._stats
        for modification in self._modification_list:
            """Iterate over each change in the modification list."""
            new_stats = new_stats.apply_modifier(modification[0])
        return new_stats

    def post_round_actions(self) -> None:
        """Update the stat modifiers by decrementing the remaining number of rounds they are in effect for."""
        for modification in self._modification_list:
            """Iterate over each change in the modification list."""
            if modification[1] - 1 == 0:
                """Suppose that the number of rounds in the modification is exhausted after using this round."""
                self._modification_list.remove(modification)
            else:
                new_modification = modification[0], modification[1] - 1
                self._modification_list.remove(modification)
                self._modification_list.append(new_modification)
        new_max_health = self.get_stats().get_max_health()
        if self._health > new_max_health:
            self._health  = new_max_health
        else:
            pass

    def rest(self) -> None:
        """Returns this pokemon to max health, removes any remaining status modifiers, and resets all move uses to their maximums."""
        self._health = self._stats.get_max_health()
        self._modification_list = []
        new_move_info = []
        for move in self._move_info:
            new_move_info.append((move[0], move[0].get_max_uses()))
        self._move_info = new_move_info

    def __str__(self) -> str:
        """(str): Returns a simple representation of this pokemons name and level."""
        return f"{self._name} (lv{self._level})"

    def __repr__(self) -> str:
        """(str): Returns a string representation of this pokemon"""
        return f"{self._name} (lv{self._level})"

class Trainer(object):
    '''A class representing a pokemon trainer. A trainer can have 6 Pokemon at maximum.'''
    def __init__(self, name: str) -> None:
        """Create an instance of the Trainer class.
        
        Parameters:
            name(str): The name of the trainer.
        """
        self._name = name
        self._inventory: Dict[Item, int] = {}
        self._all_pokemon: List[Pokemon] = []
        self.current_pokemon: Pokemon = None

    def get_name(self) -> str:
        """Return the trainer's name.
        
        Returns:
            (str): Get the name of trainer.
        """
        return self._name

    def get_inventory(self) -> Dict['Item', int]:
        """Returns the trainer's inventory as a dictionary mapping items to the count of that item remaining in the dictionary.
        
        Returns:
            (Dict['Item', int]): Get the dictionary of inventory.
        """
        return self._inventory

    def get_current_pokemon(self) -> Pokemon:
        """Gets the current pokemon, or raises a NoPokemonException if the trainer doesn't have a single pokemon.
        
        Returns:
            (Pokemon): Identify the current pokemon.
        """
        if len(self._all_pokemon) == 0:
            raise NoPokemonException()
        else:
            return self.current_pokemon

    def get_all_pokemon(self) -> List[Pokemon]:
        """Returns the trainer's pokemon.
        
        Returns:
            (List[Pokemon]): Return all pokemon, and show them in a list.
            """
        return self._all_pokemon

    def rest_all_pokemon(self) -> None:
        """Rests all pokemon in the party"""
        for pokemon in self._all_pokemon:
            """Iterate over every Pokemon of all pokemon."""
            pokemon.rest()

    def all_pokemon_fainted(self) -> bool:
        """Return true if all the trainer's pokemon have fainted.
        
        Returns:
            (bool): Identify if all the pokemon has fainted.
            """
        for pokemon in self._all_pokemon:
            if not pokemon.has_fainted():
                return False
            else:
                pass
        return True

    def can_add_pokemon(self, pokemon: Pokemon) -> bool:
        """Returns true if the supplied pokemon can be added to this trainer's roster.
        
        Parameters:
            pokemon(Pokemon): Enter the pokemon we wang to add in the list.

        Returns:
            (bool): Identify if we can add this pokemon in the list.
        """
        if pokemon not in self._all_pokemon:
            if len(self._all_pokemon) < MAXIMUM_POKEMON_ROSTER:
                """Assume that the number of Pokemon in existence is less than the maximum number of Pokemon that can be held."""
                return True
        else:
            return False

    def add_pokemon(self, pokemon: Pokemon) -> None:
        """Adds a new pokemon into the roster, assuming that doing so would be valid.

        Parameters:
            pokemon(Pokemon): Enter the pokemon we wang to add in the list.
        """
        self._all_pokemon.append(pokemon)
        if self.current_pokemon is None:
            """Assume there are no Pokemon currently."""
            self.current_pokemon = self._all_pokemon[0]

    def can_switch_pokemon(self, index: int) -> bool:
        """Determines if the pokemon index would be valid to switch to, and returns true if the switch would be valid.
        
        Parameters:
            index(int): The index of the next pokemon in the roster.
            
        Returns:
            (bool): Identify if we can switch pokemon.
        """
        if self._all_pokemon[index].has_fainted():
            """Suppose the selected Pokemon happens to faint."""
            return False
        elif self._all_pokemon[index] == self.get_current_pokemon():
            return False
        else:
            return True

    def switch_pokemon(self, index: int) -> None:
        """Switches pokemon to the one at the supplied index, assuming that the switch is valid.

        Parameters:
            index(int): The index of the pokemon to switch to.
        """
        self.current_pokemon = self._all_pokemon[index]

    def add_item(self, item: 'Item', uses: int) -> None:
        """Adds an item to the trainer's inventory and increments its uses by the supplied amount.
        Parameters:
        item('Item'): The item to add.
        uses(int): The quantity of the item to be added to the inventory.
        """
        if item not in self._inventory:
            """Imagine that the item you want to add is not in the list of items."""
            self._inventory[item] = uses
        else:
            self._inventory[item]  = self._inventory[item] + uses

    def has_item(self, item: 'Item') -> bool:
        """Returns true if the item is in the trainer's inventory and has uses.
        
        Parameters:
            item('Item'): The item in inventory.
        
        Returns:
            (bool): Identify if there are any items.
        """
        if item in self._inventory and self._inventory[item] > 0:
            """Assume that the selected item is in the list of items and the number is not zero."""
            return True
        else:
            return False

    def use_item(self, item: 'Item') -> None:
        """If the item is present in the trainer's inventory, 
            decrement its count. Removes the item from the inventory entirely if its count hits 0.
        
        Parameters:
            item('Item'): The item to use.
        """
        if item in self._inventory:
            self._inventory[item] -= 1
        else:
            pass
        if self._inventory[item] == 0:
            """Assume that the number of items selected is 0."""
            del self._inventory[item]
        else:
            pass

    def __str__(self) -> str:
        """(str): Returns a string representation of a Trainer"""
        return f"Trainer('{self._name}')"

    def __repr__(self) -> str:
        """(str): Returns a string representation of a Trainer"""
        return f"Trainer('{self._name}')"

class Battle(object):
    """A class which represents a pokemon battle."""
    def __init__(self, player: Trainer, enemy: Trainer, is_trainer_battle: bool) -> None:
        """Creates an instance of a trainer battle.
        
        Parameters:
            player(Trainer): The trainer corresponding to the player character.
            enemy(Trainer): The enemy trainer.
            is_trainer_battle(bool): True if the battle takes place between trainers.
        """
        self._player = player
        self._enemy = enemy
        self._is_trainer_battle = is_trainer_battle
        self._action_queue: List[Tuple[Action, bool]] = []
        self._trainer_queue = []
        self._end_early = False

    def get_turn(self) -> Optional[bool]:
        """Get whose turn it currently is.
        
        Returns
            (Optional[bool]): Identify whose turn it is now.
        """
        for action in self._action_queue:
            """Iterate over each action in the action list."""
            if action[1] == True:
                """The trainer that performs the action is Player."""
                return False
            else:
                pass
        return True

    def get_trainer(self, is_player: bool) -> Trainer:
        """Gets the trainer corresponding to the supplied parameter.
        
        Parameters:
            is_player(bool): True if the trainer we want is the player.
        
        Returns:
            (Trainer): Returns the trainer for the given parameters.
        """
        if is_player:
            return self._player
        else:
            return self._enemy 

    def attempt_end_early(self) -> None:
        """Ends the battle early if it's not a trainer battle."""
        if not self._is_trainer_battle:
            """Suppose it's not a fight between trainers."""
            self._end_early = True

    def is_trainer_battle(self) -> bool:
        """Returns true if the battle is between trainers.

        Returns:
            (bool): Identify if the battle is between the trainers.
        """
        return self._is_trainer_battle

    def is_action_queue_full(self) -> bool:
        """Returns true if both trainers have an action queued.
        
        Returns:
            (bool): Identify if there is move from both trainers in the queue.
        """
        if len(self._action_queue) >= 2:
            """Suppose the action queue is full of actions. Including two actions."""
            return True
        else:
            return False

    def is_action_queue_empty(self) -> bool:
        """Returns true if neither trainer have an action queued.
        
        Returns：
            (bool): Identify if the queue is empty.
        """
        if len(self._action_queue) == 0:
            """Assume there are no actions in the action queue."""
            return True
        else:
            return False
        
    def trainer_has_action_queued(self, is_player: bool) -> bool:
        """Returns true if the supplied trainer has an action queued.
        
        Parameters:
            is_player(bool): True if the trainer we want to check for is the player.
        
        Returns:
            (bool): Idetify if the trainer has move in the queue.
        """
        for action in self._action_queue:
            if action[1] == is_player:
                """Assume that the performer of the action is the Player."""
                return True
            else:
                pass
        return False

    def is_ready(self) -> bool:
        """Returns true if the next action is ready to be performed.
        
        Returns:
            (bool): Idetify if the battle is ready to do the next queue.
        """
        if self.is_over():
            """Suppose the battle is over."""
            return False
        elif len(self._action_queue) == 2 and len(self._trainer_queue) == 0:
            """There are two actions in the action queue, and no trainers in the trainer queue."""
            return True
        elif len(self._action_queue) == 1 and len(self._trainer_queue) == 1:
            """One of the trainers completes the action and enters the trainer queue."""
            return True
        else:
            return False
    
    def queue_action(self, action: 'Action', is_player: bool) -> None:
        """Attempts to queue the supplied action if it's valid given the battle state, and came from the right trainer.
        
        Parameters:
            action('Action'): The action we are attempting to queue
            is_player(bool): True if we're saying the action is going to be performed by the player. 
        """
        if action.is_valid(self, is_player=is_player):
            """The action is valid and is made by the trainer of the turn."""
            self._action_queue.append((action, is_player))
        else:
            pass

    def enact_turn(self) -> Optional['ActionSummary']:
        """Attempts to perform the next action in the queue, and returns a summary of its effects if it was valid.
        
        Returns:
            (Optional['ActionSummary']): If the move is valid, trying to perform the move.
        """
        sorted(self._action_queue, key=lambda key: key[0].get_priority())
        action = self._action_queue.pop(0)
        action_summary = action[0].apply(self, action[1])
        if action[1]:
            """Assume that the initiator of the action is Player."""
            self._trainer_queue.append(self._player)
        else:
            self._trainer_queue.append(self._enemy)
        return action_summary

    def is_over(self) -> bool:
        """Returns true if the battle is over.
        
        Returns:
            (bool): Identify if the battle is over.
        """
        if self._end_early:
            """Suppose the battle ends prematurely."""
            return True
        elif (self._player.all_pokemon_fainted()) or (self._enemy.all_pokemon_fainted()):
            return True
        else:
            return False


class ActionSummary():
    '''A class containing messages about actions and their effects.''' 
    def __init__(self, message: Optional[str] = None) -> None:
        """Constructs a new ActionSummary with an optional message.

        Parameters:
            message(Optional[str]): An optional message to be included.
        """
        self._message = []
        if message is not None:
            """Let's say the message is not empty."""
            self._message.append(message)

    def get_messages(self) -> List[str]:
        """Returns a list of the messages contained within this summary.
        
        Returns:
            (list): Get the entered message.
        """
        return self._message

    def add_message(self, message: str) -> None:
        """Adds the supplied message to the ActionSummary instance.
        
        Parameters:
            message(str):The message to add.
        """
        self._message.append(message)

    def combine(self, summary: 'ActionSummary') -> None:
        """Combines two ActionSummaries.

        Parameters:
            summary('ActionSummary'): A summary containing the messages to add.
        """
        self._message.extend(summary.get_messages())


class Action(object):
    '''An abstract class detailing anything which takes up a turn in battle.'''
    def get_priority(self) -> int:
        """Returns the priority of this action, which is used to determine which action is performed first each round in the battle.
        
        Returns:
            (int): Returns the priority of this action.
        """
        return DEFAULT_ACTION_PRIORITY

    def is_valid(self, battle: Battle, is_player: bool) -> bool:
        """Determines if the action would be valid for the given trainer and battle state. Returns true if it would be valid.
        
        Parameters:
            battle(Battle): The ongoing pokemon battle
            is_player(bool): True if the player is using this action.
            
        Returns:
            (bool): Identify if the move is valid.    
        """
        if battle.is_over(): 
            """Suppose the battle is over."""
            return False
        if len(battle._trainer_queue) != 0:
            """Assume that the trainer queue is not empty, that is, a trainer has completed the action."""
            return False
        for action in battle._action_queue:
            if action[1] == is_player:
                """The trainer that performs the action is player."""
                return False
            else:
                pass
        return True

    def apply(self, battle: Battle, is_player: bool) -> ActionSummary:
        """Applies the action to the game state and returns a summary of the effects of doing so.
        
        Parameters:
            battle(Battle): The ongoing pokemon battle
            is_player(bool): True if the player is using this action.
        
        Returns:
            (ActionSummary): Return the description of this move.
        """
        raise NotImplementedError()
    
    def __str__(self) -> str:
        """(str): Return a string representation of this class."""
        return f'{__class__.__name__}()'

    def __repr__(self) -> str:
        """(str): Return a string representation of this class."""
        return f'{__class__.__name__}()'


class Flee(Action):
    """An action where the trainer attempts to run away from the battle."""
    def is_valid(self, battle: Battle, is_player: bool) -> bool:
        """Determines if an attempt to flee would be valid for a given battle state. Returns true if it would be valid.
        
        Parameters:
            battle(Battle): The ongoing pokemon battle
            is_player(bool): True if the player is using this item.
        
        Returns:
            (bool): Identify if the escape is valid.
        """
        if not super().is_valid(battle, is_player):
            """Assume that the action is invalid."""
            return False
        elif battle.get_trainer(is_player).get_current_pokemon().has_fainted():
            """Player's current Pokemon faints during battle."""
            return False
        else:
            return True

    def apply(self, battle: Battle, is_player: bool) -> ActionSummary:
        """The trainer attempts to flee the battle.
        
        Parameters:
            battle(Battle): The ongoing pokemon battle
            is_player(bool): True if the player is using this item.
        
        Returns:
            (ActionSummary): Return the description of this flee.
        """
        action_summary = ActionSummary()
        if battle.is_trainer_battle():
            """A battle between trainers."""
            action_summary.add_message(FLEE_INVALID)
            return action_summary
        else:
            battle.attempt_end_early()
            action_summary.add_message(FLEE_SUCCESS)
            return action_summary

    def __str__(self) -> str:
        """(str): Return a string representation of this class."""
        return f'{__class__.__name__}()'

    def __repr__(self) -> str:
        """(str): Return a string representation of this class."""
        return f'{__class__.__name__}()'

class SwitchPokemon(Action):
    """An action representing the trainer's intention to switch pokemon."""
    def __init__(self, next_pokemon_index: int) -> None:
        """Creates an instance of the SwitchPokemon class.
        
        Parameters:
            next_pokemon_index(int): The index of the pokemon the trainer wants to switch to.
        """
        self._next_pokemon_index = next_pokemon_index

    def is_valid(self, battle: Battle, is_player: bool) -> bool:
        """Determines if switching pokemon would be valid for a given trainer and battle state. Returns true if it would be valid.
        
        Parameters:
            battle(Battle): The ongoing pokemon battle
            is_player(bool): True if the player is using this item.
        
        Returns:
            (bool): Identify if this move is valid.
        """
        if not super().is_valid(battle, is_player):
            """Assume that the action is invalid."""
            return False
        elif battle.get_trainer(is_player).can_switch_pokemon(self._next_pokemon_index):
            """The player can be replaced with a specific location Pokemon."""
            return True
        else:
            return False

    def apply(self, battle: Battle, is_player: bool) -> ActionSummary:
        """The trainer switches pokemon, assuming that the switch would be valid.
        
        Parameters:
            battle(Battle): The ongoing pokemon battle
            is_player(bool): True if the player is using this action.

        Returns:
            (ActionSummary): Return the description of this move.
        """
        trainer = battle.get_trainer(is_player)
        action_summary = ActionSummary()
        if is_player and not trainer.current_pokemon.has_fainted():
            """Player's turn, and his current Pokemon does not faint."""
            action_summary.add_message(f'{trainer.current_pokemon.get_name()}, return!')
        trainer.switch_pokemon(self._next_pokemon_index)
        action_summary.add_message(f'{trainer.get_name()} switched to {trainer.current_pokemon.get_name()}.')
        return action_summary
        
    def __str__(self) -> str:
        """(str): Return a string representation of this class."""
        return f'{__class__.__name__}({self._next_pokemon_index})'

    def __repr__(self) -> str:
        """(str): Return a string representation of this class."""
        return f'{__class__.__name__}({self._next_pokemon_index})'


class Item(Action):
    """An abstract class representing an Item, which a trainer may attempt to use to influence the battle."""
    def __init__(self, name: str) -> None:
        """Creates an Item.
        
        Parameters:
            name(str): The name of item.
        """
        self._name = name

    def get_name(self) -> str:
        """Return the name of this item.
        
        Returns:
            (str): Return the name of this item.
        """
        return self._name

    def is_valid(self, battle: Battle, is_player: bool) -> bool:
        """Determines if using the item would be a valid action for the given trainer and battle state.
        
        Parameters:
            battle(Battle): The ongoing pokemon battle.
            is_player(bool): True if the player is using this item.

        Returns:
            (bool): Returns true if it would be valid.
        """
        if not super().is_valid(battle, is_player):
            """Assume that the action is invalid."""
            return False
        elif (not battle.get_trainer(is_player).get_current_pokemon().has_fainted()) and (battle.get_trainer(is_player).has_item(self)):
            """Player's current Pokemon does not faint, and the number of items in the player is not zero."""
            return True
        else:
            return False

    def decrement_item_count(self, trainer: Trainer) -> None:
        """Decrease the count of this item by one in the trainer's inventory.

        Parameters:
            trainer(Trainer): The trainer attempting to use this item.
        """
        trainer.use_item(self)

    def __str__(self) -> str:
        """(str): Return a string representation of this class."""
        return f'{__class__.__name__}({self._name})'

    def __repr__(self) -> str:
        """(str): Return a string representation of this class."""
        return f'{__class__.__name__}({self._name})'


class Pokeball(Item):
    """An item which a trainer can use to attempt to catch wild pokemon."""
    def __init__(self, name: str, catch_chance: int) -> None:
        """Creates a pokeball instance, used to catch pokemon in wild battles.
        
        Parameters:
            name(str): The name of this pokeball
            catch_chance(int): The chance this pokeball has of catching a pokemon.
        """
        self._name = name
        self._catch_chance = catch_chance

    def apply(self, battle: Battle, is_player: bool) -> ActionSummary:
        """Attempt to catch the enemy pokemon and returns an ActionSummary containing information about the catch attempt.
        
        Parameters:
            battle(Battle): The ongoing pokemon battle
            is_player(bool): True if the player is using this item.
            
        Returns:
            (ActionSummary): Return the description of this process.
        """
        action_summary = ActionSummary()
        enemy_pokemon = battle.get_trainer(not is_player).get_current_pokemon()
        if battle.is_trainer_battle():
            """A battle between trainers."""
            action_summary.add_message(POKEBALL_INVALID_BATTLE_TYPE)
        else:
            if did_succeed(self._catch_chance):
                """Catch a Pokemon."""
                if battle.get_trainer(is_player).can_add_pokemon(enemy_pokemon):
                    """Assume that the player has enough room for new Pokemon."""
                    action_summary.add_message(POKEBALL_SUCCESSFUL_CATCH.format(enemy_pokemon.get_name()))
                    battle.get_trainer(is_player).add_pokemon(enemy_pokemon)
                    battle.attempt_end_early()
                else:
                    action_summary.add_message(POKEBALL_FULL_TEAM.format(enemy_pokemon.get_name()))
            else:
                action_summary.add_message(POKEBALL_UNSUCCESSFUL_CATCH.format(enemy_pokemon.get_name()))
        return action_summary
            
    def __str__(self) -> str:
        """(str): Return a string representation of this class."""
        return f"{__class__.__name__}('{self._name}')"

    def __repr__(self) -> str:
        """(str): Return a string representation of this class."""
        return f"{__class__.__name__}('{self._name}')"


class Food(Item):
    """An Item which restores HP to the pokemon whose trainer uses it."""
    def __init__(self, name: str, health_restored: int) -> None:
        """Creates a pokeball instance, used to catch pokemon in wild battles
        
        Paramters:
            name(str): The name of this pokeball
            catch_chance(int): The chance this pokeball has of catching a pokemon.
        """
        self._name = name
        self._health_restored = health_restored

    def apply(self, battle: Battle, is_player: bool) -> ActionSummary:
        """The trainer's current pokemon eats the food.
        
        Parameters:
            battle: The ongoing pokemon battle
            is_player: True if the player is using this item.
        """
        action_summary = ActionSummary()
        pokemon = battle.get_trainer(is_player).get_current_pokemon()
        pokemon.modify_health(self._health_restored)
        action_summary.add_message(f"{pokemon.get_name()} ate {self._name}.")
        return action_summary

    def __str__(self) -> str:
        """(str): Return a string representation of this class."""
        return f"{__class__.__name__}('{self._name}')"

    def __repr__(self) -> str:
        """(str): Return a string representation of this class."""
        return f"{__class__.__name__}('{self._name}')"


class Move(Action):
    """An abstract class representing all learnable pokemon moves."""
    def __init__(self, name: str, element_type: str, max_uses: int, speed: int) -> None:
        """Creates an instance of the Move class.
        
        Parameters:
            name(str): The name of this move.
            element_type(str): The name of the type of this move.
            max_uses(int): The number of time this move can be used before resting.
            speed(int): The speed of this move, with lower values corresponding to faster moves priorities.
        """
        self._name = name 
        self._element_type = element_type
        self._max_uses = max_uses
        self._speed = speed

    def get_name(self) -> str:
        """Return the name of this move.

        Returns:
            (str): Return the name of this move.
        """
        return self._name

    def get_element_type(self) -> str:
        """Return the type of this move.
        
        Returns:
            (str): Return the type of this move.
        """
        return self._element_type

    def get_max_uses(self) -> int:
        """Return the maximum times this move can be used.
        
        Returns:
            (int): Return the maximum times this move can be used.
        """
        return self._max_uses

    def get_priority(self) -> int:
        """Return the priority of this move.
        
        Returns:
            (int): Return the priority of this move.
        """
        return self._speed + SPEED_BASED_ACTION_PRIORITY

    def is_valid(self, battle: Battle, is_player: bool) -> bool:
        """Determines if the move would be valid for the given trainer and battle state.
        
        Parameters:
            battle(Battle): The ongoing pokemon battle
            is_player(bool): True if the player is using this action.
        
        Returns:
            (bool): Returns true if the move would be valid.
        """
        if super().is_valid(battle, is_player):
            """Assume that the action is invalid."""
            for move in battle.get_trainer(is_player).get_current_pokemon().get_move_info():
                """Iterate over each move in the move information list."""
                if move[0] == self and move[1] >= 1:
                    """Make sure the move is used, and that the move has enough times to use."""
                    return True
            return False
        else:
            return False

    def apply(self, battle: Battle, is_player: bool) -> ActionSummary:
        """Applies the Move to the game state.

        Parameters:
            battle(Battle): The ongoing pokemon battle
            is_player(bool): True if the player is using this action.
            
        Returns:
            (ActionSummary): Return the description of this move.
        """
        pass

    def apply_ally_effects(self, trainer: Trainer) -> ActionSummary:
        """Apply this move's effects to the ally trainer; if appropriate, and return the resulting ActionSummary.
        
        Parameters:
            trainer(Trainer): The trainer whose pokemon is using the move.
        
        Returns：
            (ActionSummary): Return the description of this move effects.
        """
        pass

    def apply_enemy_effects(self, trainer: Trainer, enemy: Trainer) -> ActionSummary:
        """Apply this move's effects to the enemy; if appropriate, and return the resulting ActionSummary.

        Parameters:
            trainer(trainer): The trainer whose pokemon is using the move.
            enemy(trainer): The trainer whose pokemon is the target of the move.
        
        Returns：
            (ActionSummary): Return the description of enemy effects.
        """
        pass

    def __str__(self):
        """(str): Return a string representation of this class."""
        return f'{self.__class__.__name__}(\'{self._name}\', \'{self._element_type}\', {self._max_uses})'

    def __repr__(self):
        """(repr): Return a string representation of this class."""
        return f'{self.__class__.__name__}(\'{self._name}\', \'{self._element_type}\', {self._max_uses})'

    def __eq__(self, other: 'Move') -> bool:
        """Identify two moves that are truly the same.
        
        Paramteters：
            other('Move'): Another move for comparison.

        Returns：
            (bool): Identify whether two moves are the same.
        """
        if self._name == other.get_name() and \
            self._element_type == other.get_element_type() and \
            self._max_uses == other.get_max_uses() and \
            self.get_priority() == other.get_priority():
            """Identify two moves that are truly the same."""
            return True
        else:
            return False


class Attack(Move):
    """A class representing damaging pokemon moves, that may be used against an enemy pokemon."""
    def __init__(self, name: str, element_type: str, max_uses: int, speed: int, base_damage: int, hit_chance: float) -> None:
        """Creates an instance of an attacking move.
        
        Parameters:
            name(str): The name of this move.
            element_type(str): The name of the type of this move.
            max_uses(int): The number of time this move can be used before resting.
            speed(int): The speed of this move, with lower values corresponding to faster moves.
            base_damage(int): The base damage of this move.
            hit_chance(float): The base hit chance of this move.
        """
        super().__init__(name, element_type, max_uses, speed)
        self._base_damage = base_damage
        self._hit_chance = hit_chance

    def did_hit(self, pokemon: Pokemon) -> bool:
        """Determine if the move hit, based on the product of the pokemon's current hit chance, and the move's hit chance.

        Paramaters：
            pokemon(Pokemon): The attacking pokemon.

        Returns：
            (bool)：Returns True if it hits.
        """
        if did_succeed(self._hit_chance * pokemon.get_stats().get_hit_chance()):
            """The move hit successfully."""
            return True
        else:
            return False

    def calculate_damage(self, pokemon: Pokemon, enemy_pokemon: Pokemon) -> int:
        """Calculates what would be the total damage of using this move, assuming it hits, 
            based on the stats of the attacking and defending pokemon.
        
        Parameters:
            pokemon(Pokemon): The attacking trainer's pokemon.
            enemy_pokemon(Pokemon): The defending trainer's pokemon.

        Returns:
            (int): Returns the number of damage.
        """
        effectiveness = ElementType.of(self._element_type).get_effectiveness(enemy_pokemon.get_element_type())
        damage = int(
            self._base_damage * effectiveness * 
            pokemon.get_stats().get_attack()/
            (enemy_pokemon.get_stats().get_defense() + 1)
        )
        return damage

    def apply(self, battle: Battle, is_player: bool) -> ActionSummary:
        action_summary = ActionSummary()
        pokemon = battle.get_trainer(is_player).get_current_pokemon()
        enemy_pokemon = battle.get_trainer(not is_player).get_current_pokemon()
        damage = self.calculate_damage(pokemon, enemy_pokemon)
        enemy_pokemon.modify_health(-damage)
        pokemon.reduce_move_count(self)
        action_summary.add_message(f'{pokemon.get_name()} used {self._name}.')
        if enemy_pokemon.has_fainted():
            """Suppose the opponent's Pokemon passes out."""
            exp = enemy_pokemon.experience_on_death()
            pokemon.gain_experience(exp)
            action_summary.add_message(f"{enemy_pokemon.get_name()} has fainted.")
            action_summary.add_message(f"{pokemon.get_name()} gained {exp} exp.")
        return action_summary


class StatusModifier(Move):
    """"An abstract class to group commonalities between buffs and debuffs."""
    def __init__(self, name: str, element_type: str, max_uses: int, speed: int,
                modification: Tuple[float, int, int, int], rounds: int) -> None:
        """Creates an instance of this class
        
        Parameters:
            name(str): The name of this move
            element_type(str): The name of the type of this move
            max_uses(int): The number of time this move can be used before resting
            speed(int): The speed of this move, with lower values corresponding to faster moves.
            modification(Tuple[float, int, int, int]): A list of the same structure as the PokemonStats, 
                                                    to be applied for the duration of the supplied number of rounds.
            rounds(int): The number of rounds for the modification to be in effect.
        """
        self._name = name 
        self._element_type = element_type
        self._max_uses = max_uses
        self._speed = speed
        self._modification = modification
        self._rounds = rounds

class Buff(StatusModifier):
    """Moves which buff the trainer's selected pokemon."""
    pass


class Debuff(StatusModifier):
    """Moves which debuff the enemy trainer's selected pokemon."""
    pass


# Below are the classes and functions which pertain only to masters students.
class Strategy(object):
    """An abstract class providing behaviour to determine a next action given a battle state."""
    def get_next_action(self, battle: Battle, is_player: bool) -> Action:
        """Determines and returns the next action for this strategy, given the battle state and trainer.
        
        Parameters:
            battle(Battle): The ongoing pokemon battle
            is_player(bool): True if the player is using this action.
        
        Returns:
            (Action): Action taken in battle。
        """
        raise NotImplementedError()


class ScaredyCat(Strategy):
    """A strategy where the trainer always attempts to flee."""
    pass


class TeamRocket(Strategy):
    """A tough strategy used by Pokemon Trainers that are members of Team Rocket."""
    pass


def create_encounter(trainer: Trainer, wild_pokemon: Pokemon) -> Battle:
    """Creates a Battle corresponding to an encounter with a wild pokemon.
    
    Parameters:
        trainer(Trainer): The adventuring trainer.
        wild_pokemon(Pokemon): The pokemon that the player comes into contact with.
        
    Returns:
        (Battle): Returns new battle.
    """
    pass


if __name__ == "__main__":
    # print(WRONG_FILE_MESSAGE)
    pass