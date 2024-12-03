# gui_manager.py

import pygame
import sys

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
        self.load_assets()
        self.font = pygame.font.SysFont(None, 36)

    def load_assets(self):
        # Load images and other assets
        self.assets['dice_faces'] = {}
        for i in range(1, 7):
            image = pygame.image.load(f'images/dice/dice_face_{i}.png').convert_alpha()
            self.assets['dice_faces'][i] = pygame.transform.scale(image, (64, 64))

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

    def create_button(self, rect, text, callback, font_size=36):
        return self.Button(self, rect, text, callback, font_size)
