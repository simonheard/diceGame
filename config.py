# config.py

# Set to True to enable debug mode
# In debug mode
# - AI player's dice and scores are displayed
DEBUG = False  

# Initial player tokens
INITIAL_TOKENS = 20

# Power-up settings
POWERUP_SETTINGS = {
    'reroll_single_dice': {
        'name': 'Reroll Single Dice',
        'price_range': (5, 10)
    },
    'double_tokens_if_win': {
        'name': 'Double Tokens If Win',
        'price_range': (15, 25)
    },
    'set_dice_to_one': {
        'name': 'Set Dice to 1',
        'price_range': (10, 20)
    },
    'set_dice_to_number': {
        'name': 'Set Dice to Desired Number',
        'price_range': (20, 30)
    }
}

# Level configurations
LEVELS = {
    1: {
        'base_entry': 5,
        'base_reward': 10,
        'description': 'Easy',
        'ai_stop_threshold': (60, 90),
        'dice_probabilities': None  # Fair roll
    },
    2: {
        'base_entry': 10,
        'base_reward': 25,
        'description': 'Medium',
        'ai_stop_threshold': (80, 110),
        'dice_probabilities': [25, 10, 10, 15, 15, 25]  # Probabilities for 1-6
    },
    3: {
        'base_entry': 20,
        'base_reward': 60,
        'description': 'Hard',
        'ai_stop_threshold': (100, 140),
        'dice_probabilities': [40, 5, 5, 10, 10, 30]
    }
}

# Multipliers available
MULTIPLIERS = [1, 2, 5, 10, 20, 30, 50, 100]

# Other game settings
MINIMUM_TOKENS_TO_PLAY = 5  # Minimum tokens required to play

# Shop settings
SHOP_REFRESH_RATE = 1  # How often the shop prices refresh (e.g., after each game)
