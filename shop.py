# shop.py

import random
import config  # Import config.py

class Shop:
    def __init__(self):
        self.powerups = config.POWERUP_SETTINGS
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
