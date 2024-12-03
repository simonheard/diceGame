# dice_game.py

from player import Player, AIPlayer
from score_calculator import ScoreCalculator
import pygame
import sys
import math  # Import math module for rounding up

class DiceGame:
    def __init__(self, gui, player_tokens, opponent, entry_tokens, reward_tokens, debug=False):
        self.gui = gui
        self.player = Player("Player")
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

    def start(self):
        # Initialize both players' dice
        self.player.roll_dice()
        self.opponent.roll_dice()

        while not self.game_over:
            if self.current_turn == "player":
                if not self.player_stopped:
                    self.player_stopped = self.player_turn()
                    if self.player_stopped:
                        # Player has stopped, AI gets one final turn
                        self.current_turn = "opponent"
                    else:
                        # Switch to opponent's turn
                        self.current_turn = "opponent"
                else:
                    # Player has stopped, check if AI has also stopped
                    if self.opponent_stopped:
                        self.game_over = True
                    else:
                        # AI gets one more turn after player stops
                        self.current_turn = "opponent"
            elif self.current_turn == "opponent":
                if not self.opponent_stopped:
                    self.opponent_stopped = self.opponent_turn()
                    if self.opponent_stopped:
                        # Notify player that AI has stopped
                        self.notify_ai_stopped()
                        if self.player_stopped:
                            self.game_over = True
                        else:
                            # Player gets one final turn
                            self.player_final_turn = True
                            self.current_turn = "player"
                    else:
                        if self.player_stopped:
                            # AI has taken its final turn after player stopped
                            self.game_over = True
                        else:
                            # Switch to player's turn
                            self.current_turn = "player"
                else:
                    if self.player_stopped:
                        self.game_over = True
                    else:
                        # Switch to player's turn
                        self.current_turn = "player"

        # After the loop ends, compare scores
        winner = self.compare_scores()
        self.display_scores(winner)
        # Update player tokens based on the result
        if winner == "player":
            self.player_tokens += self.reward_tokens
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
        self.gui.clear_screen()
        self.gui.display_message("Your Turn", (50, 30))
        self.gui.display_dice(self.player.get_dice_values(), (50, 80))
        self.gui.display_message(f"Current Score: {self.player.score}", (50, 180))

        # Create buttons for actions
        if self.player_final_turn:
            action_message = "Final Turn! Choose an action."
        else:
            action_message = "Choose an action."
        self.gui.display_message(action_message, (50, 220))

        reroll_button = self.gui.create_button((50, 260, 150, 50), "Reroll", self.set_player_action_reroll)
        stop_button = self.gui.create_button((220, 260, 150, 50), "Stop", self.set_player_action_stop)

        buttons = [reroll_button, stop_button]

        self.player_action = None

        while self.player_action is None:
            self.gui.clear_screen()
            self.gui.display_message("Your Turn", (50, 30))
            self.gui.display_dice(self.player.get_dice_values(), (50, 80))
            self.gui.display_message(f"Current Score: {self.player.score}", (50, 180))
            self.gui.display_message(action_message, (50, 220))

            for button in buttons:
                button.draw()

            self.gui.update_screen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                for button in buttons:
                    button.handle_event(event)
            self.gui.clock.tick(60)

        if self.player_action == 'reroll':
            self.player.roll_dice()  # For simplicity, reroll all dice
            if self.player_final_turn:
                # Player has taken their final turn
                return True  # Player must stop after this
            else:
                return False  # Player did not stop
        elif self.player_action == 'stop':
            return True  # Player chose to stop

    def set_player_action_reroll(self):
        self.player_action = 'reroll'

    def set_player_action_stop(self):
        self.player_action = 'stop'

    def opponent_turn(self):
        # Returns True if opponent chooses to stop, False otherwise
        self.opponent.calculate_score(self.score_calculator)
        self.gui.clear_screen()
        self.gui.display_message(f"{self.opponent.name}'s Turn", (50, 30))

        if self.debug:
            # In debug mode, display AI's dice and score
            self.gui.display_dice(self.opponent.get_dice_values(), (50, 80))
            self.gui.display_message(f"Current Score: {self.opponent.score}", (50, 180))
        else:
            # Hide AI's dice and score
            self.gui.display_message("AI is thinking...", (50, 80))

        self.gui.update_screen()
        pygame.time.wait(1000)  # Wait 1 second to simulate thinking

        # Handle events during AI's turn to prevent crashes
        self.handle_ai_events()

        self.opponent.decide_to_reroll(self.score_calculator)
        if self.opponent.has_stopped:
            return True  # Opponent chose to stop
        else:
            if self.player_stopped:
                # If player has stopped, AI gets only one more reroll
                self.opponent.roll_dice()
                self.opponent.calculate_score(self.score_calculator)
                return True  # AI must stop after this reroll
            else:
                self.opponent.roll_dice()
                return False  # Opponent did not stop

    def notify_ai_stopped(self):
        self.gui.clear_screen()
        self.gui.display_message(f"{self.opponent.name} has stopped.", (50, 200))
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
            # Display player's dice and score
            self.gui.display_message("Final Results", (50, 20), font_size=48)
            self.gui.display_message("Your Dice:", (50, 80))
            self.gui.display_dice(self.player.get_dice_values(), (50, 120))
            self.gui.display_message(f"Your Score: {self.player.score}", (50, 200))

            # Display AI's dice and score
            self.gui.display_message(f"{self.opponent.name}'s Dice:", (600, 80))
            self.gui.display_dice(self.opponent.get_dice_values(), (600, 120))
            self.gui.display_message(f"{self.opponent.name}'s Score: {self.opponent.score}", (600, 200))

            if winner == "player":
                result_message = "You Win!"
                tokens_message = f"You won {self.reward_tokens} tokens."
            elif winner == "opponent":
                result_message = "You Lose!"
                tokens_message = f"You lost your entry tokens."
            else:
                result_message = "It's a Draw!"
                refund = math.ceil(self.entry_tokens * 0.8)
                tokens_message = f"You receive {refund} tokens back."

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
