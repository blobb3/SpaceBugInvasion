import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game, image_path, hit_points):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and set its rect attribute
        self.image = pygame.image.load(image_path)
        self.original_image = self.image  # Keep the original image to scale
        self.rect = self.image.get_rect()

        # Set the life points based on the image path
        self.hit_points = hit_points
        self.max_hit_points = hit_points

        # Scale the image to fit within the maximum size without distortion
        self.scale_image()

        # Initialize position
        self.rect.x = 0
        self.rect.y = 0
        self.x = float(self.rect.x)  # Store the alien's exact horizontal position

    def scale_image(self):
        """Scale the alien image to fit within the maximum size without distortion."""
        max_width, max_height = self.settings.alien_max_size
        original_width, original_height = self.original_image.get_width(), self.original_image.get_height()
        
        # Calculate scaling factor while maintaining the aspect ratio
        scale_factor = min(max_width / original_width, max_height / original_height)
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        
        # Scale the image
        self.image = pygame.transform.scale(self.original_image, (new_width, new_height))
        self.rect = self.image.get_rect()

    def take_hit(self):
        """Reduce hit points and check if the alien is destroyed."""
        self.hit_points -= 1
        return self.hit_points <= 0

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        """Move the alien to the right or left."""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def draw(self):
        """Draw the alien and its health bar on the screen."""
        self.screen.blit(self.image, self.rect)
        self.draw_health_bar()

    def draw_health_bar(self):
        """Draw a health bar over the alien to show its remaining hit points."""
        if self.hit_points < self.max_hit_points:
            bar_length = 30  
            bar_height = 5  
            fill = (self.hit_points / self.max_hit_points) * bar_length
            health_bar_rect = pygame.Rect(0, 0, bar_length, bar_height)
            fill_rect = pygame.Rect(0, 0, fill, bar_height)
            health_bar_rect.centerx = self.rect.centerx
            health_bar_rect.top = self.rect.top - 10  
            pygame.draw.rect(self.screen, (255, 0, 0), fill_rect.move(health_bar_rect.topleft))
            pygame.draw.rect(self.screen, (255, 255, 255), health_bar_rect, 1)
