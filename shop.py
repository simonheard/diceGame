# shop.py

import random

class Shop:
    def __init__(self):
        self.powerups = {
            'reroll_single_dice': {'name': 'Reroll Single Dice', 'price_range': (5, 10)},
            'double_tokens_if_win': {'name': 'Double Tokens If Win', 'price_range': (15, 25)},
            'set_dice_to_one': {'name': 'Set Dice to 1', 'price_range': (10, 20)},
            'set_dice_to_number': {'name': 'Set Dice to Desired Number', 'price_range': (20, 30)},
        }
        self.prices = {}
        self.generate_prices()

    def generate_prices(self):
        for key, value in self.powerups.items():
            self.prices[key] = random.randint(*value['price_range'])

    def purchase_powerup(self, powerup_key, player_tokens):
        price = self.prices[powerup_key]
        if player_tokens >= price:
            return price  # Return the price to deduct
        else:
            return None  # Not enough tokens
