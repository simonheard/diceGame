# game.py

from gui_manager import GUIManager
from player import Player, AIPlayer
from dice_game import DiceGame
import pygame
import sys

class Game:
    def __init__(self):
        self.gui = GUIManager()
        self.player_tokens = 20
        self.current_opponent = None

    def start(self):
        while True:
            # Check if player tokens are zero or negative
            if self.player_tokens <= 0:
                self.display_game_over()
                pygame.quit()
                sys.exit()
            self.gui.clear_screen()
            self.display_main_menu()
            self.gui.update_screen()
            action = self.handle_main_menu_input()
            if action == 'play':
                self.choose_opponent()
            elif action == 'quit':
                pygame.quit()
                sys.exit()

    def display_main_menu(self):
        # Display the main menu options
        self.gui.display_message(f"Tokens: {self.player_tokens}", (50, 30))
        options = [
            "P. Play Game",
            "Q. Quit"
        ]
        self.gui.display_menu(options)

    def handle_main_menu_input(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        return 'play'
                    elif event.key == pygame.K_q:
                        return 'quit'
            self.gui.clock.tick(60)

    def choose_opponent(self):
        selected_level, selected_multiplier = self.select_level_and_multiplier()
        if selected_level is None or selected_multiplier is None:
            return  # User cancelled selection

        levels = {
            1: {'base_entry': 5, 'base_reward': 10},
            2: {'base_entry': 10, 'base_reward': 25},
            3: {'base_entry': 20, 'base_reward': 60}
        }
        base_entry_tokens = levels[selected_level]['base_entry']
        base_reward_tokens = levels[selected_level]['base_reward']

        entry_tokens = base_entry_tokens * selected_multiplier
        reward_tokens = base_reward_tokens * selected_multiplier

        if self.player_tokens >= entry_tokens:
            self.player_tokens -= entry_tokens
            self.current_opponent = AIPlayer(f"Level {selected_level} AI", selected_level)
            debug_mode = False  # Set to True to enable debug mode
            dice_game = DiceGame(self.gui, self.player_tokens, self.current_opponent, entry_tokens, reward_tokens, debug=debug_mode)
            self.player_tokens = dice_game.start()
        else:
            # Not enough tokens, display a message
            self.gui.clear_screen()
            self.gui.display_message("Not enough tokens!", (50, 200), font_size=48, color=(255, 0, 0))
            self.gui.update_screen()
            pygame.time.wait(2000)  # Wait 2 seconds

    def select_level_and_multiplier(self):
        levels = {
            1: {'base_entry': 5, 'base_reward': 10},
            2: {'base_entry': 10, 'base_reward': 25},
            3: {'base_entry': 20, 'base_reward': 60}
        }
        multipliers = [1, 2, 5, 10, 20, 50, 100]
        selected_level_index = 0  # Index in levels list
        selected_multiplier_index = 0  # Index in multipliers list

        level_keys = list(levels.keys())

        while True:
            self.gui.clear_screen()
            self.gui.display_message("Select Level and Multiplier", (50, 30))

            # Display Level Options
            for idx, level in enumerate(level_keys):
                prefix = "-> " if idx == selected_level_index else "   "
                self.gui.display_message(f"{prefix}Level {level}", (50, 80 + idx * 40))

            # Display Multiplier Options
            for idx, multiplier in enumerate(multipliers):
                prefix = "-> " if idx == selected_multiplier_index else "   "
                self.gui.display_message(f"{prefix}{multiplier}x", (250, 80 + idx * 40))

            # Calculate required tokens
            selected_level = level_keys[selected_level_index]
            selected_multiplier = multipliers[selected_multiplier_index]

            base_entry_tokens = levels[selected_level]['base_entry']
            required_tokens = base_entry_tokens * selected_multiplier

            # Display required tokens
            self.gui.display_message(f"Tokens Required: {required_tokens}", (50, 400))

            # Display current tokens
            self.gui.display_message(f"Your Tokens: {self.player_tokens}", (50, 450))

            self.gui.display_message("Use Arrow Keys to Select, Enter to Start, Esc to Cancel", (50, 500))

            self.gui.update_screen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        # Move level selection up
                        if selected_level_index > 0:
                            selected_level_index -= 1
                    elif event.key == pygame.K_DOWN:
                        # Move level selection down
                        if selected_level_index < len(level_keys) - 1:
                            selected_level_index += 1
                    elif event.key == pygame.K_LEFT:
                        # Move multiplier selection left
                        if selected_multiplier_index > 0:
                            selected_multiplier_index -= 1
                    elif event.key == pygame.K_RIGHT:
                        # Move multiplier selection right
                        if selected_multiplier_index < len(multipliers) - 1:
                            selected_multiplier_index += 1
                    elif event.key == pygame.K_RETURN:
                        # Check if player has enough tokens
                        if self.player_tokens >= required_tokens:
                            return selected_level, selected_multiplier
                        else:
                            # Not enough tokens
                            self.gui.display_message("Not enough tokens!", (50, 550), font_size=48, color=(255, 0, 0))
                            self.gui.update_screen()
                            pygame.time.wait(2000)
                    elif event.key == pygame.K_ESCAPE:
                        # Cancel and return to main menu
                        return None, None
            self.gui.clock.tick(60)

    def display_game_over(self):
        self.gui.clear_screen()
        self.gui.display_message("Game Over!", (200, 250), font_size=72, color=(255, 0, 0))
        self.gui.display_message("You have run out of tokens.", (180, 320), font_size=36)
        self.gui.update_screen()
        pygame.time.wait(5000)  # Wait 5 seconds before closing
