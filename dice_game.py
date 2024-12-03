# dice_game.py

import pygame
import sys
import math
import random
from player import Player, AIPlayer
from score_calculator import ScoreCalculator
import config  # Import config.py

class DiceGame:
    def __init__(self, gui, player_tokens, opponent, entry_tokens, reward_tokens, debug=False, player=None):
        self.gui = gui
        self.player = player if player else Player("Player")  # Use the player from game.py
        self.opponent = opponent
        self.score_calculator = ScoreCalculator()
        self.player_tokens = player_tokens
        self.entry_tokens = entry_tokens
        self.reward_tokens = reward_tokens
        self.current_turn = "player"
        self.player_stopped = False
        self.opponent_stopped = False
        self.game_over = False
        self.debug = debug  # Add debug flag
        self.player_final_turn = False  # Flag to indicate if player is on final turn
        self.return_to_menu_clicked = False  # Initialize flag
        self.double_reward_multiplier = 1  # Multiplier for double tokens power-up

    def start(self):
        # Initialize both players' dice without playing dice roll sound
        self.player.roll_dice()
        self.opponent.roll_dice()

        while not self.game_over:
            if self.current_turn == "player":
                if not self.player_stopped:
                    self.player_stopped = self.player_turn()
                    self.current_turn = "opponent"
                elif self.player_final_turn:
                    # Player gets final turn after AI stops
                    self.player_final_turn = False  # Reset the flag
                    self.player_stopped = self.player_turn()
                    self.game_over = True  # Game ends after player's final turn
                else:
                    self.game_over = True  # Both players have stopped
            elif self.current_turn == "opponent":
                if not self.opponent_stopped:
                    self.opponent_stopped = self.opponent_turn()
                    if self.opponent_stopped:
                        self.notify_ai_stopped()
                        if not self.player_stopped:
                            # Player gets one final turn
                            self.player_final_turn = True
                            self.current_turn = "player"
                        else:
                            self.game_over = True
                    else:
                        self.current_turn = "player"
                else:
                    if self.player_stopped:
                        self.game_over = True
                    else:
                        # Player gets one final turn
                        self.player_final_turn = True
                        self.current_turn = "player"

        # After the loop ends, compare scores
        winner = self.compare_scores()
        self.display_scores(winner)
        # Update player tokens based on the result
        if winner == "player":
            total_reward = self.reward_tokens * self.double_reward_multiplier
            self.player_tokens += total_reward
        elif winner == "draw":
            # Return 80% of the entry tokens, rounded up
            refund = math.ceil(self.entry_tokens * 0.8)
            self.player_tokens += refund
        # If the player loses, tokens are already deducted
        # Return the updated token count
        return self.player_tokens

    def player_turn(self):
        # Returns True if player chooses to stop, False otherwise
        self.player.calculate_score(self.score_calculator)
        self.player_action = None
        self.selected_powerup = None

        while True:
            self.gui.clear_screen()
            self.display_player_info()
            self.display_ai_status()

            if self.player_final_turn:
                action_message = "Final Turn! Choose an action."
            else:
                action_message = "Choose an action."
            self.gui.display_message(action_message, (50, 220))

            # Create action buttons
            reroll_button = self.gui.create_button((50, 260, 150, 50), "Reroll", self.set_player_action_reroll)
            stop_button = self.gui.create_button((220, 260, 150, 50), "Stop", self.set_player_action_stop)

            buttons = [reroll_button, stop_button]

            # Create power-up buttons directly on the main action screen
            powerup_buttons = []
            y_position = 330
            for idx, (key, quantity) in enumerate(self.player.inventory.items()):
                if quantity > 0:
                    powerup_name = self.gui.powerup_names[key]
                    powerup_image = self.gui.assets['powerups'][key]
                    button = self.gui.create_image_button(
                        (50, y_position + idx * 100, 300, 90),
                        powerup_image,
                        f"{powerup_name} ({quantity})",
                        lambda p_key=key: self.use_powerup(p_key)
                    )
                    powerup_buttons.append(button)

            buttons.extend(powerup_buttons)

            # Draw all buttons
            for button in buttons:
                button.draw()

            self.gui.update_screen()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                for button in buttons:
                    button.handle_event(event)

            # Handle player action
            if self.player_action == 'reroll':
                # Animate dice reroll
                self.gui.animate_dice_reroll(num_dice=5, position=(50, 70))
                # Perform the actual reroll
                self.player.roll_dice()
                # Recalculate the score after reroll
                self.player.calculate_score(self.score_calculator)
                if self.player_final_turn:
                    # Player has taken their final turn
                    return True  # Player must stop after this
                else:
                    return False  # Player did not stop
            elif self.player_action == 'stop':
                return True  # Player chose to stop

            # Reset player_action for next iteration
            self.player_action = None

            self.gui.clock.tick(60)

    def set_player_action_reroll(self):
        self.player_action = 'reroll'

    def set_player_action_stop(self):
        self.player_action = 'stop'

    def use_powerup(self, powerup_key):
        if self.player.inventory[powerup_key] <= 0:
            # No power-ups of this type left
            return

        # Play power-up apply sound
        self.gui.sounds['powerup_use'].play()

        if powerup_key == 'reroll_single_dice':
            # Ask the player which dice to reroll
            dice_index = self.gui.select_dice("Select a dice to reroll:", self.player.get_dice_values())
            if dice_index is not None:
                self.player.use_powerup(powerup_key, dice_index)
                # Recalculate the score after using the power-up
                self.player.calculate_score(self.score_calculator)
        elif powerup_key == 'set_dice_to_one':
            # Ask the player which dice to set to 1
            dice_index = self.gui.select_dice("Select a dice to set to ①:", self.player.get_dice_values())
            if dice_index is not None:
                self.player.use_powerup(powerup_key, dice_index)
                # Recalculate the score after using the power-up
                self.player.calculate_score(self.score_calculator)
        elif powerup_key == 'set_dice_to_number':
            # Ask the player which dice and what number
            dice_index = self.gui.select_dice("Select a dice to set to desired number:", self.player.get_dice_values())
            desired_number = self.gui.select_number("Select the desired number (1-6):")
            if dice_index is not None and desired_number is not None:
                self.player.use_powerup(powerup_key, dice_index, desired_number)
                # Recalculate the score after using the power-up
                self.player.calculate_score(self.score_calculator)
        elif powerup_key == 'double_tokens_if_win':
            # Use the power-up
            self.player.use_powerup(powerup_key)
            self.double_reward_multiplier *= 2  # Multiply the reward multiplier

    def opponent_turn(self):
        # Returns True if opponent chooses to stop, False otherwise
        self.opponent.calculate_score(self.score_calculator)
        self.gui.clear_screen()
        self.display_player_info()  # Always display player's info
        self.display_ai_status()    # Display AI status

        self.gui.update_screen()
        pygame.time.wait(500)  # Wait 0.5 seconds to simulate thinking

        # Handle events during AI's turn to prevent crashes
        self.handle_ai_events()

        self.opponent.decide_to_reroll(self.score_calculator)
        if self.opponent.has_stopped:
            return True  # Opponent chose to stop
        else:
            # Animate dice reroll for AI (optional)
            if not self.debug:
                self.gui.animate_dice_reroll(num_dice=5, position=(600, 70))
            # Perform the actual reroll
            self.opponent.roll_dice()
            # Removed redundant dice roll sound
            # self.gui.sounds['dice_roll'].play()
            self.opponent.calculate_score(self.score_calculator)
            if self.player_stopped:
                # If player has stopped, AI must stop after this reroll
                return True
            else:
                return False  # Opponent did not stop

    def notify_ai_stopped(self):
        self.gui.clear_screen()
        self.display_player_info()  # Always display player's info
        self.display_ai_status()
        self.gui.display_message(f"{self.opponent.name} has stopped.", (600, 300))
        self.gui.update_screen()
        pygame.time.wait(2000)  # Wait 2 seconds

    def compare_scores(self):
        if self.player.score > self.opponent.score:
            return "player"
        elif self.player.score < self.opponent.score:
            return "opponent"
        else:
            return "draw"

    def display_scores(self, winner):
        self.return_to_menu_clicked = False  # Initialize flag

        while not self.return_to_menu_clicked:
            self.gui.clear_screen()
            # Display "Final Results" at the top
            self.gui.display_message("Final Results", (50, 20), font_size=48)

            # Display player's dice and score
            self.gui.display_message("Your Dice:", (50, 80))
            self.gui.display_dice(self.player.get_dice_values(), (50, 120))
            self.gui.display_message(f"Your Score: {self.player.score}", (50, 200))

            # Display AI's dice and score (always show in final results)
            self.gui.display_message(f"{self.opponent.name}'s Dice:", (600, 80))
            self.gui.display_dice(self.opponent.get_dice_values(), (600, 120))
            self.gui.display_message(f"{self.opponent.name}'s Score: {self.opponent.score}", (600, 200))

            if winner == "player":
                result_message = "You Win!"
                total_reward = self.reward_tokens * self.double_reward_multiplier
                tokens_message = f"You won {total_reward} tokens!"
            elif winner == "opponent":
                result_message = "You Lose!"
                tokens_message = f"You lost your entry tokens."
            else:
                result_message = "It's a Draw!"
                refund = math.ceil(self.entry_tokens * 0.8)
                tokens_message = f"You receive {refund} tokens back."

            # Move the result messages down to allow enough space above
            self.gui.display_message(result_message, (50, 250), font_size=48)
            self.gui.display_message(tokens_message, (50, 300))

            # Create 'Main Menu' button
            main_menu_button = self.gui.create_button((412, 500, 200, 50), "Main Menu", self.return_to_main_menu)
            main_menu_button.draw()

            self.gui.update_screen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                main_menu_button.handle_event(event)
            self.gui.clock.tick(60)

    def return_to_main_menu(self):
        # Set a flag to exit the loop
        self.return_to_menu_clicked = True

    def handle_ai_events(self):
        # Handle events during AI's turn to prevent crashes
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Ignore other events during AI's turn

    def display_player_info(self):
        """Helper method to display player's dice and score."""
        self.gui.display_message("Your Dice:", (50, 30))
        self.gui.display_dice(self.player.get_dice_values(), (50, 70))
        self.gui.display_message(f"Current Score: {self.player.score}", (50, 160))

    def display_ai_status(self):
        """Helper method to display AI's status."""
        self.gui.display_message(f"{self.opponent.name}'s Status:", (600, 30))
        if self.debug:
            # Display AI's dice and score in debug mode
            self.gui.display_dice(self.opponent.get_dice_values(), (600, 70))
            self.gui.display_message(f"AI Score: {self.opponent.score}", (600, 160))
        else:
            # Hide AI's dice and scores during gameplay
            status = "AI has stopped." if self.opponent_stopped else "AI is playing."
            self.gui.display_message(status, (600, 70))
