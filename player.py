# player.py

from dice import DiceSet
import random
import config

class Player:
    def __init__(self, name):
        self.name = name
        self.dice_set = DiceSet()  # Initialize the dice set
        self.score = 0
        self.inventory = {
            'reroll_single_dice': 0,
            'double_tokens_if_win': 0,
            'set_dice_to_one': 0,
            'set_dice_to_number': 0
        }

    def roll_dice(self):
        # Roll all dice
        self.dice_set.roll_all()
        # Update dice values
        self.dice_values = self.dice_set.get_values()

    def get_dice_values(self):
        # Return the current dice values
        return self.dice_set.get_values()

    def calculate_score(self, score_calculator):
        # Calculate the score based on current dice values
        self.dice_values = self.dice_set.get_values()
        self.score = score_calculator.calculate_score(self.dice_values)

    def use_powerup(self, powerup_type, *args):
        # Logic to use a power-up
        if self.inventory[powerup_type] > 0:
            self.inventory[powerup_type] -= 1
            # Implement power-up effect
            if powerup_type == 'reroll_single_dice':
                dice_index = args[0]
                # Reroll a single dice
                self.dice_set.reroll_selected([dice_index])
            elif powerup_type == 'double_tokens_if_win':
                # This power-up is applied at the end of the game
                pass
            elif powerup_type == 'set_dice_to_one':
                dice_index = args[0]
                self.dice_set.set_dice_value(dice_index, 1)
            elif powerup_type == 'set_dice_to_number':
                dice_index = args[0]
                desired_number = args[1]
                self.dice_set.set_dice_value(dice_index, desired_number)
            return True
        else:
            return False  # Power-up not available

    def add_powerup(self, powerup_type, quantity=1):
        self.inventory[powerup_type] += quantity


class AIPlayer(Player):
    def __init__(self, name, level):
        super().__init__(name)
        self.level = level
        self.stop_threshold = self.set_stop_threshold()
        self.dice_probabilities = self.set_dice_probabilities()
        self.has_stopped = False  # Initialize has_stopped
        self.dice_set = DiceSet()  # Initialize the dice set

    def set_stop_threshold(self):
        level_config = config.LEVELS[self.level]
        return random.randint(*level_config['ai_stop_threshold'])

    def set_dice_probabilities(self):
        level_config = config.LEVELS[self.level]
        return level_config['dice_probabilities']

    def roll_dice(self):
        self.dice_set.roll_all(self.dice_probabilities)
        # Update dice values
        self.dice_values = self.dice_set.get_values()

    def decide_to_reroll(self, score_calculator):
        # AI decides whether to reroll based on current score
        self.calculate_score(score_calculator)
        if self.score >= self.stop_threshold:
            self.has_stopped = True
        else:
            self.has_stopped = False

    def calculate_score(self, score_calculator):
        # Calculate the score based on current dice values
        self.dice_values = self.dice_set.get_values()
        self.score = score_calculator.calculate_score(self.dice_values)
