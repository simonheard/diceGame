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
        if self.player_final_turn:
            self.gui.display_message("Final Turn! Press 'R' to reroll or 'S' to stop.", (50, 220))
        else:
            self.gui.display_message("Press 'R' to reroll or 'S' to stop.", (50, 220))
        self.gui.update_screen()
        action = self.get_player_action()
        if action == 'reroll':
            self.player.roll_dice()  # For simplicity, reroll all dice
            if self.player_final_turn:
                # Player has taken their final turn
                return True  # Player must stop after this
            else:
                return False  # Player did not stop
        elif action == 'stop':
            return True  # Player chose to stop

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
        self.gui.clear_screen()
        # Display player's dice and score
        self.gui.display_message("Final Results", (50, 20), font_size=48)
        self.gui.display_message("Your Dice:", (50, 80))
        self.gui.display_dice(self.player.get_dice_values(), (50, 120))
        self.gui.display_message(f"Your Score: {self.player.score}", (50, 200))

        # Display AI's dice and score
        self.gui.display_message(f"{self.opponent.name}'s Dice:", (400, 80))
        self.gui.display_dice(self.opponent.get_dice_values(), (400, 120))
        self.gui.display_message(f"{self.opponent.name}'s Score: {self.opponent.score}", (400, 200))

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
        self.gui.display_message("Press 'M' to return to the main menu.", (50, 350))
        self.gui.update_screen()
        self.wait_for_main_menu()

    def get_player_action(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return 'reroll'
                    elif event.key == pygame.K_s:
                        return 'stop'
            self.gui.clock.tick(60)

    def wait_for_main_menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        return
            self.gui.clock.tick(60)

    def handle_ai_events(self):
        # Handle events during AI's turn to prevent crashes
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Ignore other events during AI's turn
