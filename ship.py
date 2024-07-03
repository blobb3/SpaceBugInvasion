import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """A class to manage the ship"""

    def __init__ (self, ai_game):
        """Initialize the ship and set its starting position"""
        super().__init__()
        self.screen =  ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect
        self.image = pygame.image.load('images/ship6.png')

        # Scale the image to be 10 times smaller
        original_width = self.image.get_width()
        original_height = self.image.get_height()
        new_width = original_width // 4
        new_height = original_height // 4
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

        # Get the rect of the scaled image
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a float for the ship's exact horizontal positon
        self.x = float(self.rect.x)

        # Movement flag; start with a ship that is not moving
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's position based on the movement flag -> moves the ship right or left when the flag is TRUE"""
        # Update the ships x value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Update rect object form self.x
        self.rect.x = self.x

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect) # python treats all elements as rectangles

    def center_ship(self):
        """Center the ship on the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)