# game.py

from gui_manager import GUIManager
from player import Player, AIPlayer
from dice_game import DiceGame
import pygame
import sys
from shop import Shop
import config  # Import config.py

class Game:
    def __init__(self):
        self.gui = GUIManager()
        self.player_tokens = config.INITIAL_TOKENS  # Starting tokens
        self.current_opponent = None
        self.running = True  # Game loop control
        self.back_to_menu = False
        self.restart_clicked = False
        self.last_selected_level = None
        self.last_selected_multiplier = None
        self.shop = Shop()
        self.player = Player("Player")
        self.gui.play_bgm(volume=config.BGM_VOLUME)  # Play the background music on game start

    def start(self):
        while self.running:
            if self.player_tokens < 5:
                self.display_game_over()
                if self.restart_clicked:
                    self.restart_clicked = False
                    continue
                else:
                    break
            self.main_menu()

    def main_menu(self):
        self.gui.clear_screen()
        self.gui.display_message(f"Tokens: {self.player_tokens}", (50, 30))

        # Define buttons
        play_button = self.gui.create_button((412, 200, 200, 50), "Play Game", self.choose_opponent)
        shop_button = self.gui.create_button((412, 300, 200, 50), "Shop", self.open_shop)
        rules_button = self.gui.create_button((412, 400, 200, 50), "Game Rules", self.show_rules_and_credits)
        quit_button = self.gui.create_button((412, 500, 200, 50), "Quit", self.quit_game)

        buttons = [play_button, shop_button, rules_button, quit_button]
        
        while self.running:
            if self.player_tokens < config.MINIMUM_TOKENS_TO_PLAY:
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
            
    def show_rules_and_credits(self):
        # Navigate to the rules and credits page
        self.display_rules_and_credits()

    def display_rules_and_credits(self):
        back_button = self.gui.create_button((412, 650, 200, 50), "Back", self.exit_rules_and_credits)

        self.back_to_menu = False  # Ensure the flag is reset
        running = True
        while running:
            self.gui.clear_screen()
            
            game_rule_section_offsets = [50, 30]
            credit_section_offsets = [500, 30]
            line_height = 50
            small_font_line_height = 30

            # Game Rules Section
            self.gui.display_message("Game Rules", 
                                    (game_rule_section_offsets[0], game_rule_section_offsets[1]), 
                                    font_size=48)
            self.gui.display_message("1. Roll dice to score points.", 
                                    (game_rule_section_offsets[0], game_rule_section_offsets[1] + line_height), 
                                    font_size=36)
            self.gui.display_message("2. High scores are earned through:", 
                                    (game_rule_section_offsets[0], game_rule_section_offsets[1] + 2 * line_height), 
                                    font_size=36)
            self.gui.display_message("- 1-2-3-4-5 straight: 130 points", 
                                    (game_rule_section_offsets[0] + 20, game_rule_section_offsets[1] + 3 * line_height), 
                                    font_size=30)
            self.gui.display_message("- 2-3-4-5-6 straight: 110 points", 
                                    (game_rule_section_offsets[0] + 20, game_rule_section_offsets[1] + 3 * line_height + small_font_line_height), 
                                    font_size=30)
            self.gui.display_message("- Dice face 1 acts as a wildcard ", 
                                    (game_rule_section_offsets[0] + 20, game_rule_section_offsets[1] + 3 * line_height + 2 * small_font_line_height), 
                                    font_size=30)
            self.gui.display_message("  when not used in a straight.", 
                                    (game_rule_section_offsets[0] + 50, game_rule_section_offsets[1] + 3 * line_height + 3 * small_font_line_height), 
                                    font_size=30)
            self.gui.display_message("- Five of a kind: 100 + dice sum", 
                                    (game_rule_section_offsets[0] + 20, game_rule_section_offsets[1] + 3 * line_height + 4 * small_font_line_height), 
                                    font_size=30)
            self.gui.display_message("- Full House (3+2 same): 70 + dice sum", 
                                    (game_rule_section_offsets[0] + 20, game_rule_section_offsets[1] + 3 * line_height + 5 * small_font_line_height), 
                                    font_size=30)
            self.gui.display_message("- Four of a kind: 70 + dice sum", 
                                    (game_rule_section_offsets[0] + 20, game_rule_section_offsets[1] + 3 * line_height + 6 * small_font_line_height), 
                                    font_size=30)
            self.gui.display_message("- Three of a kind or Two Pairs:", 
                                    (game_rule_section_offsets[0] + 20, game_rule_section_offsets[1] + 3 * line_height + 7 * small_font_line_height), 
                                    font_size=30)
            self.gui.display_message("  40 + dice sum", 
                                    (game_rule_section_offsets[0] + 50, game_rule_section_offsets[1] + 3 * line_height + 8 * small_font_line_height), 
                                    font_size=30)
            self.gui.display_message("- One Pair: 10 + dice sum", 
                                    (game_rule_section_offsets[0] + 20, game_rule_section_offsets[1] + 3 * line_height + 9 * small_font_line_height), 
                                    font_size=30)
            self.gui.display_message("3. Use power-ups strategically to gain advantage.", 
                                    (game_rule_section_offsets[0], game_rule_section_offsets[1] + 4 * line_height + 9 * small_font_line_height), 
                                    font_size=36)
            self.gui.display_message("4. Win tokens by defeating AI opponents.",
                                    (game_rule_section_offsets[0], game_rule_section_offsets[1] + 5 * line_height + 9 * small_font_line_height),
                                    font_size=36)
            self.gui.display_message("5. Get tokens as much as you can to keep playing!",
                                    (game_rule_section_offsets[0], game_rule_section_offsets[1] + 6 * line_height + 9 * small_font_line_height),
                                    font_size=36)

            # Credits Section
            self.gui.display_message("Credits", 
                                    (credit_section_offsets[0], credit_section_offsets[1]), 
                                    font_size=48)
            self.gui.display_message("Game developed by: Hede Wang", 
                                    (credit_section_offsets[0], credit_section_offsets[1] + line_height), 
                                    font_size=36)
            self.gui.display_message("BGM: Created with Suno AI", 
                                    (credit_section_offsets[0], credit_section_offsets[1] + 2 * line_height), 
                                    font_size=36)
            self.gui.display_message("Sound effects: Hede Wang / Pixabay", 
                                    (credit_section_offsets[0], credit_section_offsets[1] + 3 * line_height), 
                                    font_size=36)



            back_button.draw()
            self.gui.update_screen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                back_button.handle_event(event)

            # Move this condition inside the while loop
            if self.back_to_menu:
                running = False  # Exit the rules and credits page

            self.gui.clock.tick(60)

    def exit_rules_and_credits(self):
        self.back_to_menu = True

    def choose_opponent(self):
        self.select_level_and_multiplier()
        if self.back_to_menu:
            self.back_to_menu = False  # Reset the flag here
            return  # Return to main menu
        if self.selected_level is None or self.selected_multiplier is None:
            return  # User cancelled selection or did not confirm

        levels = config.LEVELS  # Use levels from config
        base_entry_tokens = levels[self.selected_level]['base_entry']
        base_reward_tokens = levels[self.selected_level]['base_reward']

        entry_tokens = base_entry_tokens * self.selected_multiplier
        reward_tokens = base_reward_tokens * self.selected_multiplier

        if self.player_tokens >= entry_tokens:
            self.player_tokens -= entry_tokens
            self.current_opponent = AIPlayer(f"Level {self.selected_level} AI", self.selected_level)
            debug_mode = False  # Set to True to enable debug mode
            dice_game = DiceGame(
                self.gui,
                self.player_tokens,
                self.current_opponent,
                entry_tokens,
                reward_tokens,
                debug=config.DEBUG,
                player=self.player  # Pass the player instance
            )
            self.player_tokens = dice_game.start()
            # Generate new shop prices after the game
            self.shop.generate_prices()
        else:
            # Not enough tokens, display a message
            self.gui.clear_screen()
            self.gui.display_message("Not enough tokens!", (50, 200), font_size=48, color=(255, 0, 0))
            self.gui.update_screen()
            pygame.time.wait(2000)  # Wait 2 seconds

    def select_level_and_multiplier(self):
        levels = config.LEVELS
        multipliers = config.MULTIPLIERS  # Including 30x multiplier

        self.selected_level = self.last_selected_level
        self.selected_multiplier = self.last_selected_multiplier
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
                # Display level description
                level_desc = levels[self.selected_level]['description']
                self.gui.display_message(f"Difficulty: {level_desc}", (100, 300), font_size=24)

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

            if self.back_to_menu:
                return  # Return to main menu

            self.gui.clock.tick(60)

        # After exiting the loop
        if self.back_to_menu:
            return  # Return to main menu

        if self.selected_level and self.selected_multiplier:
            # Remember the player's selection
            self.last_selected_level = self.selected_level
            self.last_selected_multiplier = self.selected_multiplier

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
        # Reset back_to_menu flag at the start
        self.back_to_menu = False

        shopping = True

        while shopping:
            self.gui.clear_screen()
            self.gui.display_message("Shop", (50, 30), font_size=48)
            self.gui.display_message(f"Your Tokens: {self.player_tokens}", (50, 80))

            # Display power-ups and prices
            powerup_buttons = []
            y_position = 130
            for idx, (key, powerup) in enumerate(self.shop.powerups.items()):
                price = self.shop.prices[key]
                player_quantity = self.player.inventory.get(key, 0)
                button_text = f"{powerup['name']} - {price} tokens (You have: {player_quantity})"
                # Create image buttons for power-ups
                button = self.gui.create_image_button(
                    (50, y_position + idx * 100, 300, 90),
                    self.gui.load_image(f'images/powerups/{key}.png'),
                    button_text,
                    lambda p_key=key: self.purchase_powerup(p_key)
                )
                powerup_buttons.append(button)

            # Back button
            back_button = self.gui.create_button((50, 600, 200, 50), "Back", self.back_to_main_menu)
            buttons = powerup_buttons + [back_button]

            # Draw buttons
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

            if self.back_to_menu:
                self.back_to_menu = False  # Reset the flag
                shopping = False  # Exit the shop

            self.gui.clock.tick(60)

    def purchase_powerup(self, powerup_key):
        price = self.shop.prices[powerup_key]
        if self.player_tokens >= price:
            self.player_tokens -= price
            self.player.add_powerup(powerup_key)
            # Play power-up purchase sound
            self.gui.sounds['purchase'].play()
            # Directly update the shop display without showing a confirmation screen
        else:
            # Not enough tokens
            self.gui.clear_screen()
            self.gui.display_message("Not enough tokens!", (50, 200), font_size=48, color=(255, 0, 0))
            self.gui.update_screen()
            pygame.time.wait(2000)

    def quit_game(self):
        self.gui.stop_bgm()  # Stop the background music on quit
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
        self.player_tokens = config.INITIAL_TOKENS  # Reset tokens to starting amount
        self.restart_clicked = True  # Set flag to exit the loop
        # Reset last selected level and multiplier
        self.last_selected_level = None
        self.last_selected_multiplier = None
        # Reset player's inventory
        self.player.inventory = {
            'reroll_single_dice': 0,
            'double_tokens_if_win': 0,
            'set_dice_to_one': 0,
            'set_dice_to_number': 0
        }
