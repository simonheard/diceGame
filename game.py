# game.py

from gui_manager import GUIManager
from player import Player, AIPlayer
from dice_game import DiceGame
import pygame
import sys

class Game:
    def __init__(self):
        self.gui = GUIManager()
        self.player_tokens = 20  # Starting tokens
        self.current_opponent = None
        self.running = True  # Game loop control
        self.back_to_menu = False  # Add back_to_menu flag
        self.restart_clicked = False  # Initialize restart flag

    def start(self):
        while self.running:
            # Check if player tokens are less than 5 (minimum required to play)
            if self.player_tokens < 5:
                self.display_game_over()
                # After game over, check if restart was clicked
                if self.restart_clicked:
                    # Reset tokens already done in restart_game
                    self.restart_clicked = False  # Reset the flag
                    continue  # Continue the game loop
                else:
                    # Not restarting, exit the game
                    break
            self.main_menu()

    def main_menu(self):
        self.gui.clear_screen()
        self.gui.display_message(f"Tokens: {self.player_tokens}", (50, 30))

        # Define buttons
        play_button = self.gui.create_button((412, 200, 200, 50), "Play Game", self.choose_opponent)
        shop_button = self.gui.create_button((412, 300, 200, 50), "Shop", self.open_shop)
        quit_button = self.gui.create_button((412, 400, 200, 50), "Quit", self.quit_game)

        buttons = [play_button, shop_button, quit_button]

        while self.running:
            if self.player_tokens < 5:
                self.display_game_over()
                # After game over, check if restart was clicked
                if self.restart_clicked:
                    self.restart_clicked = False  # Reset the flag
                    continue  # Restart the main menu loop
                else:
                    # Not restarting, exit the game
                    break

            self.gui.clear_screen()
            self.gui.display_message(f"Tokens: {self.player_tokens}", (50, 30))
            for button in buttons:
                button.draw()
            self.gui.update_screen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                for button in buttons:
                    button.handle_event(event)
            self.gui.clock.tick(60)

    def choose_opponent(self):
        self.select_level_and_multiplier()
        if self.back_to_menu:
            return  # Return to main menu
        if self.selected_level is None or self.selected_multiplier is None:
            return  # User cancelled selection or did not confirm

        levels = {
            1: {'base_entry': 5, 'base_reward': 10},
            2: {'base_entry': 10, 'base_reward': 25},
            3: {'base_entry': 20, 'base_reward': 60}
        }
        base_entry_tokens = levels[self.selected_level]['base_entry']
        base_reward_tokens = levels[self.selected_level]['base_reward']

        entry_tokens = base_entry_tokens * self.selected_multiplier
        reward_tokens = base_reward_tokens * self.selected_multiplier

        if self.player_tokens >= entry_tokens:
            self.player_tokens -= entry_tokens
            self.current_opponent = AIPlayer(f"Level {self.selected_level} AI", self.selected_level)
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
        multipliers = [1, 2, 5, 10, 20, 30, 50, 100]  # Including 30x multiplier

        self.selected_level = None
        self.selected_multiplier = None
        self.confirm_clicked = False
        self.back_to_menu = False  # Reset back_to_menu flag

        # Adjusted button sizes
        level_button_width = 200
        level_button_height = 50  # Shorter height
        multiplier_button_width = 150
        multiplier_button_height = 50  # Shorter height

        # Create level buttons
        level_buttons = []
        for idx, level in enumerate(levels.keys()):
            button = self.gui.create_button(
                (100, 100 + idx * (level_button_height + 10), level_button_width, level_button_height),
                f"Level {level}",
                lambda lvl=level: self.set_selected_level(lvl)
            )
            level_buttons.append(button)

        # Create multiplier buttons in two columns
        multiplier_buttons = []
        for idx, multiplier in enumerate(multipliers):
            x_position = 400 + (idx % 2) * (multiplier_button_width + 20)
            y_position = 100 + (idx // 2) * (multiplier_button_height + 10)
            button = self.gui.create_button(
                (x_position, y_position, multiplier_button_width, multiplier_button_height),
                f"{multiplier}x",
                lambda mult=multiplier: self.set_selected_multiplier(mult)
            )
            multiplier_buttons.append(button)

        # Confirm and Back buttons
        confirm_button = self.gui.create_button((700, 600, 200, 50), "Confirm", self.confirm_selection)
        back_button = self.gui.create_button((100, 600, 200, 50), "Back", self.back_to_main_menu)

        buttons = level_buttons + multiplier_buttons + [confirm_button, back_button]

        while not self.confirm_clicked and not self.back_to_menu:
            self.gui.clear_screen()
            self.gui.display_message("Select Level and Multiplier", (50, 30))

            # Draw buttons
            for button in buttons:
                button.draw()

            # Provide visual feedback for selections
            if self.selected_level:
                idx = list(levels.keys()).index(self.selected_level)
                pygame.draw.rect(self.gui.screen, (0, 255, 0), level_buttons[idx].rect, 3)  # Green border

            if self.selected_multiplier:
                idx = multipliers.index(self.selected_multiplier)
                pygame.draw.rect(self.gui.screen, (0, 255, 0), multiplier_buttons[idx].rect, 3)  # Green border

            # Display required tokens if selections are made
            tokens_color = (255, 255, 255)  # Default color (white)
            confirm_button.enabled = True  # Enable confirm button by default

            if self.selected_level and self.selected_multiplier:
                base_entry_tokens = levels[self.selected_level]['base_entry']
                required_tokens = base_entry_tokens * self.selected_multiplier
                if self.player_tokens >= required_tokens:
                    tokens_color = (255, 255, 255)  # White color if sufficient tokens
                    confirm_button.enabled = True
                else:
                    tokens_color = (255, 0, 0)  # Red color if insufficient tokens
                    confirm_button.enabled = False  # Disable confirm button

                self.gui.display_message(f"Tokens Required: {required_tokens}", (50, 500), color=tokens_color)
                self.gui.display_message(f"Your Tokens: {self.player_tokens}", (50, 450))
            else:
                self.gui.display_message("Please select both level and multiplier.", (50, 500))
                confirm_button.enabled = False  # Disable confirm button if selections incomplete

            self.gui.update_screen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                for button in buttons:
                    button.handle_event(event)

            self.gui.clock.tick(60)

        # After exiting the loop
        if self.back_to_menu:
            return  # Return to main menu

        if self.selected_level and self.selected_multiplier:
            base_entry_tokens = levels[self.selected_level]['base_entry']
            required_tokens = base_entry_tokens * self.selected_multiplier
            if self.player_tokens >= required_tokens:
                # Proceed to start the game
                return
            else:
                # Not enough tokens
                self.gui.clear_screen()
                self.gui.display_message("Not enough tokens!", (50, 550), font_size=48, color=(255, 0, 0))
                self.gui.update_screen()
                pygame.time.wait(2000)
                self.confirm_clicked = False
                self.select_level_and_multiplier()
        else:
            # Selections not complete
            self.gui.clear_screen()
            self.gui.display_message("Please select both level and multiplier.", (50, 550), font_size=36, color=(255, 0, 0))
            self.gui.update_screen()
            pygame.time.wait(2000)
            self.confirm_clicked = False
            self.select_level_and_multiplier()

    def set_selected_level(self, level):
        self.selected_level = level

    def set_selected_multiplier(self, multiplier):
        self.selected_multiplier = multiplier

    def confirm_selection(self):
        self.confirm_clicked = True  # Set a flag to exit the selection loop

    def back_to_main_menu(self):
        self.selected_level = None
        self.selected_multiplier = None
        self.confirm_clicked = True  # Exit the selection loop
        self.back_to_menu = True  # Indicate we are returning to main menu

    def open_shop(self):
        # Placeholder for shop implementation
        self.gui.clear_screen()
        self.gui.display_message("Shop is under construction!", (200, 250), font_size=48, color=(255, 255, 0))
        self.gui.display_message("Press any key to return to the main menu.", (180, 320), font_size=36)
        self.gui.update_screen()
        self.wait_for_keypress()

    def wait_for_keypress(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
            self.gui.clock.tick(60)

    def quit_game(self):
        self.running = False
        pygame.quit()
        sys.exit()

    def display_game_over(self):
        # Display Game Over screen with a Restart button
        self.gui.clear_screen()
        self.gui.display_message("Game Over!", (300, 200), font_size=72, color=(255, 0, 0))
        self.gui.display_message("You have run out of tokens.", (320, 300), font_size=36)
        restart_button = self.gui.create_button((412, 400, 200, 50), "Restart", self.restart_game)
        quit_button = self.gui.create_button((412, 500, 200, 50), "Quit", self.quit_game)
        buttons = [restart_button, quit_button]
        self.gui.update_screen()

        self.restart_clicked = False  # Initialize flag
        game_over = True
        while game_over:
            self.gui.clear_screen()
            self.gui.display_message("Game Over!", (300, 200), font_size=72, color=(255, 0, 0))
            self.gui.display_message("You have run out of tokens.", (320, 300), font_size=36)
            for button in buttons:
                button.draw()
            self.gui.update_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                for button in buttons:
                    button.handle_event(event)
            self.gui.clock.tick(60)
            if self.restart_clicked or not self.running:
                game_over = False  # Exit the loop if restart clicked or game is quitting

    def restart_game(self):
        self.player_tokens = 20  # Reset tokens to starting amount
        self.restart_clicked = True  # Set flag to exit the loop
