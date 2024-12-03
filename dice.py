# dice.py

import random

class Dice:
    def __init__(self):
        self.face_value = None

    def roll(self, probabilities=None):
        if probabilities:
            # Use weighted probabilities for dice roll
            self.face_value = random.choices(
                population=[1, 2, 3, 4, 5, 6],
                weights=probabilities,
                k=1
            )[0]
        else:
            # Standard fair roll
            self.face_value = random.randint(1, 6)

    def set_face_value(self, value):
        self.face_value = value

    def get_face_value(self):
        return self.face_value

class DiceSet:
    def __init__(self, num_dice=5):
        self.dice = [Dice() for _ in range(num_dice)]

    def roll_all(self, probabilities=None):
        for die in self.dice:
            die.roll(probabilities)

    def reroll_selected(self, indices, probabilities=None):
        for index in indices:
            self.dice[index].roll(probabilities)

    def set_dice_value(self, index, value):
        self.dice[index].set_face_value(value)

    def get_values(self):
        return [die.get_face_value() for die in self.dice]
