import random
import pygame
from alien import Alien

class Fleet:
    """A class to manage the fleet of aliens."""

    def __init__(self, ai_game):
        """Initialize the fleet and set its starting position."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.aliens = ai_game.aliens
        self.ship = ai_game.ship
        self.stats = ai_game.stats

    def create_fleet(self):
        """Create a fleet of aliens."""
        alien = Alien(self.ai_game, 'images/alien1.png', 1)  # Temporary alien for size measurement
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        available_space_y = self.settings.screen_height - self.settings.header_height - (3 * alien_height) - self.ship.rect.height
        number_rows = available_space_y // (2 * alien_height)

        alien_images = {
            'images/alien1.png': 1,
            'images/alien2.png': 2,
            'images/alien3.png': 3,
            'images/alien4.png': 4,
            'images/alien5.png': 5
        }

        # Determine available alien images based on the current level
        available_images = {img: hp for img, hp in alien_images.items()
                            if hp <= 3 or (self.stats.level >= 3 and hp == 4) or (self.stats.level >= 4 and hp == 5)}

        # Create the fleet with the available alien images
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                image_path, hit_points = random.choice(list(available_images.items()))
                self._create_alien(alien_number, row_number, image_path, hit_points)

    def _create_alien(self, alien_number, row_number, image_path, hit_points):
        """Create an alien and place it in the fleet."""
        alien = Alien(self.ai_game, image_path, hit_points)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = self.settings.header_height + alien_height + 2 * alien_height * row_number
        self.aliens.add(alien)

    def check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
