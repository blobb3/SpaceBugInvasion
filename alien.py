import pygame

from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('images/alien.png')

        # Scale the image to be the same size as the ship's image.
        original_width = self.image.get_width()
        original_height = self.image.get_height()
        new_width = original_width // 8
        new_height = original_height // 8
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

        self.rect = self.image.get_rect()

        # Start each new alien at the top left of the screen.
        self.rect.x = 0
        self.rect.y = 0

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)
