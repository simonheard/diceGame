# gui_manager.py

import pygame
import sys

class GUIManager:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (30, 30, 30)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Dice Game")
        self.clock = pygame.time.Clock()
        self.assets = {}
        self.load_assets()
        self.font = pygame.font.SysFont(None, 36)

    def load_assets(self):
        # Load images and other assets
        self.assets['dice_faces'] = {}
        for i in range(1, 7):
            image = pygame.image.load(f'images/dice/dice_face_{i}.png').convert_alpha()
            self.assets['dice_faces'][i] = pygame.transform.scale(image, (64, 64))

        # Load buttons and other UI elements as needed

    def display_dice(self, dice_values, position):
        # Display the dice images based on the values
        for idx, value in enumerate(dice_values):
            x = position[0] + idx * 70  # Adjust spacing as needed
            y = position[1]
            dice_image = self.assets['dice_faces'][value]
            self.screen.blit(dice_image, (x, y))

    def update_screen(self):
        pygame.display.flip()
        self.clock.tick(60)  # Limit to 60 FPS

    def display_message(self, message, position, font_size=36, color=(255, 255, 255)):
        font = pygame.font.SysFont(None, font_size)
        text_surface = font.render(message, True, color)
        self.screen.blit(text_surface, position)

    def get_player_input(self):
        # Handle events and return player actions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Handle other events like mouse clicks, key presses, etc.

    def display_menu(self, options):
        # Render a menu with the given options
        # For now, we'll just display the options as text
        for idx, option in enumerate(options):
            self.display_message(option, (50, 100 + idx * 40))

    def get_menu_selection(self):
        # Retrieve the player's menu choice
        # Placeholder for menu selection logic
        pass

    def clear_screen(self):
        self.screen.fill(self.bg_color)  # Clear the screen with background color
