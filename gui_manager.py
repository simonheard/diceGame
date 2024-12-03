# gui_manager.py

import pygame
import sys
import random

class GUIManager:
    def __init__(self):
        pygame.init()
        self.screen_width = 1024  # Increased width
        self.screen_height = 768  # Increased height
        self.bg_color = (30, 30, 30)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Dice Game")
        self.clock = pygame.time.Clock()
        self.assets = {}
        self.font = pygame.font.SysFont(None, 36)
        self.powerup_names = {
            'reroll_single_dice': 'Reroll Single Dice',
            'double_tokens_if_win': 'Double Tokens If Win',
            'set_dice_to_one': 'Set Dice to ①',
            'set_dice_to_number': 'Set Dice to Desired Number'
        }
        self.load_assets()  # Moved after defining powerup_names

    def load_assets(self):
        # Load images and other assets
        self.assets['dice_faces'] = {}
        for i in range(1, 7):
            image = pygame.image.load(f'images/dice/dice_face_{i}.png').convert_alpha()
            self.assets['dice_faces'][i] = pygame.transform.scale(image, (64, 64))
        # Load power-up images
        self.assets['powerups'] = {}
        for key in self.powerup_names.keys():
            image = pygame.image.load(f'images/powerups/{key}.png').convert_alpha()
            self.assets['powerups'][key] = image  # Keep original size

    def load_image(self, path):
        image = pygame.image.load(path).convert_alpha()
        return image

    def display_dice(self, dice_values, position):
        # Display the dice images based on the values
        for idx, value in enumerate(dice_values):
            x = position[0] + idx * 80  # Adjusted spacing
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

    def clear_screen(self):
        self.screen.fill(self.bg_color)  # Clear the screen with background color

    class Button:
        def __init__(self, gui_manager, rect, text, callback, font_size=36):
            self.gui_manager = gui_manager
            self.rect = pygame.Rect(rect)
            self.text = text
            self.callback = callback
            self.font = pygame.font.SysFont(None, font_size)
            self.base_color = (70, 70, 70)
            self.hover_color = (100, 100, 100)
            self.disabled_color = (50, 50, 50)
            self.current_color = self.base_color
            self.text_color = (255, 255, 255)
            self.enabled = True  # Add enabled attribute

        def draw(self):
            color = self.current_color
            if not self.enabled:
                color = self.disabled_color
            pygame.draw.rect(self.gui_manager.screen, color, self.rect)
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            self.gui_manager.screen.blit(text_surface, text_rect)

        def handle_event(self, event):
            if not self.enabled:
                return
            if event.type == pygame.MOUSEMOTION:
                if self.rect.collidepoint(event.pos):
                    self.current_color = self.hover_color
                else:
                    self.current_color = self.base_color
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.callback()

    class ImageButton:
        def __init__(self, gui_manager, rect, image, text, callback, font_size=24):
            self.gui_manager = gui_manager
            self.rect = pygame.Rect(rect)
            self.image = image
            self.text = text
            self.callback = callback
            self.font = pygame.font.SysFont(None, font_size)
            self.base_color = (70, 70, 70)
            self.hover_color = (100, 100, 100)
            self.current_color = self.base_color
            self.text_color = (255, 255, 255)
            self.enabled = True  # Add enabled attribute

            # Scale the image to fit within the button while preserving aspect ratio
            max_image_width = self.rect.width - 20
            max_image_height = self.rect.height - 40
            image_rect = self.image.get_rect()
            scale_ratio = min(max_image_width / image_rect.width, max_image_height / image_rect.height)
            new_width = int(image_rect.width * scale_ratio)
            new_height = int(image_rect.height * scale_ratio)
            self.image = pygame.transform.scale(self.image, (new_width, new_height))

        def draw(self):
            color = self.current_color
            if not self.enabled:
                color = self.base_color
            pygame.draw.rect(self.gui_manager.screen, color, self.rect)
            # Center the image
            image_rect = self.image.get_rect()
            image_rect.centerx = self.rect.centerx
            image_rect.top = self.rect.top + 5
            self.gui_manager.screen.blit(self.image, image_rect)
            # Draw text below the image
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.bottom - 20))
            self.gui_manager.screen.blit(text_surface, text_rect)

        def handle_event(self, event):
            if not self.enabled:
                return
            if event.type == pygame.MOUSEMOTION:
                if self.rect.collidepoint(event.pos):
                    self.current_color = self.hover_color
                else:
                    self.current_color = self.base_color
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.callback()

    def create_button(self, rect, text, callback, font_size=36):
        return self.Button(self, rect, text, callback, font_size)

    def create_image_button(self, rect, image, text, callback, font_size=24):
        return self.ImageButton(self, rect, image, text, callback, font_size)

    # New method for dice reroll animation
    def animate_dice_reroll(self, num_dice, position, duration=500, fps=30):
        """
        Animate the dice reroll by rapidly changing dice faces.

        Args:
            num_dice (int): Number of dice to animate.
            position (tuple): Starting (x, y) position to display the dice.
            duration (int): Total duration of the animation in milliseconds.
            fps (int): Frames per second for the animation.
        """
        frames = int(duration / (1000 / fps))
        clock = pygame.time.Clock()

        for _ in range(frames):
            self.clear_screen()
            # Randomize dice values for animation
            dice_values = [random.randint(1, 6) for _ in range(num_dice)]
            self.display_dice(dice_values, position)
            pygame.display.flip()
            clock.tick(fps)

    def select_dice(self, message, dice_values):
        """
        Display a prompt to select a dice.

        Args:
            message (str): The prompt message.
            dice_values (list): Current dice values.

        Returns:
            int: Index of the selected dice (0-4), or None if canceled.
        """
        selecting = True
        selected_dice = None
        font = pygame.font.SysFont(None, 36)

        while selecting:
            self.clear_screen()
            self.display_message(message, (50, 30))
            self.display_dice(dice_values, (50, 80))

            # Highlight the dice when hovered
            mouse_pos = pygame.mouse.get_pos()
            for idx in range(len(dice_values)):
                x = 50 + idx * 80
                y = 80
                dice_rect = pygame.Rect(x, y, 64, 64)
                if dice_rect.collidepoint(mouse_pos):
                    pygame.draw.rect(self.screen, (255, 255, 0), dice_rect, 2)
                else:
                    pygame.draw.rect(self.screen, (255, 255, 255), dice_rect, 1)

            self.update_screen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for idx in range(len(dice_values)):
                        x = 50 + idx * 80
                        y = 80
                        dice_rect = pygame.Rect(x, y, 64, 64)
                        if dice_rect.collidepoint(event.pos):
                            selected_dice = idx
                            selecting = False
                            break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        selecting = False
                        break
            self.clock.tick(60)

        return selected_dice

    def select_number(self, message):
        """
        Display a prompt to select a number between 1 and 6.

        Args:
            message (str): The prompt message.

        Returns:
            int: The selected number (1-6), or None if canceled.
        """
        selecting = True
        selected_number = None
        font = pygame.font.SysFont(None, 36)

        # Create buttons for numbers 1 to 6
        number_buttons = []
        for i in range(1, 7):
            x = 50 + (i - 1) * 80
            y = 80
            button = self.create_button((x, y, 60, 60), str(i), lambda num=i: self.set_selected_number(num))
            number_buttons.append(button)

        self.selected_number = None

        while selecting:
            self.clear_screen()
            self.display_message(message, (50, 30))

            for button in number_buttons:
                button.draw()

            self.update_screen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                for button in number_buttons:
                    button.handle_event(event)
                if self.selected_number is not None:
                    selected_number = self.selected_number
                    selecting = False
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        selecting = False
                        break
            self.clock.tick(60)

        return selected_number

    def set_selected_number(self, number):
        self.selected_number = number
