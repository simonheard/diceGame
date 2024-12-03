# player.py

from dice import DiceSet
import random

class Player:
    def __init__(self, name):
        self.name = name
        self.dice_set = DiceSet()
        self.score = 0
        self.has_stopped = False

    def roll_dice(self):
        self.dice_set.roll_all()

    def decide_to_reroll(self):
        # Placeholder for GUI interaction
        pass

    def decide_to_stop(self):
        # Placeholder for GUI interaction
        pass

    def get_dice_values(self):
        return self.dice_set.get_values()

    def calculate_score(self, score_calculator):
        dice_values = self.get_dice_values()
        self.score = score_calculator.calculate_score(dice_values)

class AIPlayer(Player):
    def __init__(self, name, level):
        super().__init__(name)
        self.level = level
        self.stop_threshold = self.set_stop_threshold()
        self.dice_probabilities = self.set_dice_probabilities()

    def set_stop_threshold(self):
        if self.level == 1:
            return random.randint(70, 100)
        elif self.level == 2:
            return random.randint(90, 120)
        elif self.level == 3:
            return random.randint(110, 150)

    def set_dice_probabilities(self):
        if self.level == 1:
            return None  # Fair roll
        elif self.level == 2:
            # Level 2 probabilities: 15% for 2-5, 20% for 1 and 6
            return [20, 15, 15, 15, 15, 20]
        elif self.level == 3:
            # Level 3 probabilities: 25% for 1 and 6, 15% for 4 and 5, 10% for 2 and 3
            return [25, 10, 10, 15, 15, 25]

    def roll_dice(self):
        self.dice_set.roll_all(self.dice_probabilities)

    def decide_to_reroll(self, score_calculator):
        # AI decides whether to reroll based on current score
        self.calculate_score(score_calculator)
        if self.score >= self.stop_threshold:
            self.has_stopped = True
        else:
            self.has_stopped = False

    def calculate_score(self, score_calculator):
        # Use the same method as the parent class
        super().calculate_score(score_calculator)
