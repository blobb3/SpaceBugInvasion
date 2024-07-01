import pygame

class Ship:
    """A class to manage the ship"""

    def __init__ (self, ai_game):
        """Initialize the ship and set its starting position"""
        self.screen =  ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect
        self.image = pygame.image.load('images/ship6.png')

        # Scale the image to be 10 times smaller
        original_width = self.image.get_width()
        original_height = self.image.get_height()
        new_width = original_width // 8
        new_height = original_height // 8
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

        # Get the rect of the scaled image
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect) # python treats all elements as rectangles
