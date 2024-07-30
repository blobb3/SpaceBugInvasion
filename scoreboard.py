import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard:
    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        self.label_font = pygame.font.SysFont(None, 24)

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Turn the score into a rendered image."""
        score_str = "{:,}".format(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color)
        self.score_image_rect = self.score_image.get_rect()

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score_str = "{:,}".format(self.stats.high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)
        self.high_score_rect = self.high_score_image.get_rect()

    def prep_level(self):
        """Turn the level into a rendered image"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color)
        self.level_rect = self.level_image.get_rect()

    def prep_ships(self):
        """Show how many ships are left"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.image = pygame.image.load('images/ship_life.png')
            ship_height = self.score_image_rect.height
            ship.image = self.scale_image(ship.image, ship_height, ship_height)
            ship.rect = ship.image.get_rect()
            ship.rect.x = 0  # Temporary positioning
            ship.rect.y = 0
            self.ships.add(ship)

    def scale_image(self, image, new_width, new_height):
        """Scale the image to the specified width and height."""
        return pygame.transform.scale(image, (new_width, new_height))

    def show_score(self):
        """Draw scores, level, and ships to the screen."""
        # Draw background for the header
        header_color = (30, 30, 30)
        header_rect = pygame.Rect(0, 0, self.screen_rect.width, self.settings.header_height)
        pygame.draw.rect(self.screen, header_color, header_rect)

        # Draw border around the header
        border_color = (255, 210, 0)
        border_thickness = 4
        pygame.draw.rect(self.screen, border_color, header_rect, border_thickness)

        # Calculate spacing
        padding = 20
        label_padding = 5
        element_width = self.screen_rect.width // 4

        # Draw labels and center them
        score_label = self.label_font.render("Score", True, self.text_color, header_color)
        score_label_rect = score_label.get_rect(center=(padding + element_width // 2, padding + score_label.get_height() // 2))
        self.screen.blit(score_label, score_label_rect)

        high_score_label = self.label_font.render("High Score", True, self.text_color, header_color)
        high_score_label_rect = high_score_label.get_rect(center=(element_width + padding + element_width // 2, padding + high_score_label.get_height() // 2))
        self.screen.blit(high_score_label, high_score_label_rect)

        lives_label = self.label_font.render("Lives", True, self.text_color, header_color)
        lives_label_rect = lives_label.get_rect(center=(2 * element_width + padding + element_width // 2, padding + lives_label.get_height() // 2))
        self.screen.blit(lives_label, lives_label_rect)

        level_label = self.label_font.render("Level", True, self.text_color, header_color)
        level_label_rect = level_label.get_rect(center=(3 * element_width + padding + element_width // 2, padding + level_label.get_height() // 2))
        self.screen.blit(level_label, level_label_rect)

        # Position score text
        self.score_image_rect.centerx = score_label_rect.centerx
        self.score_image_rect.top = score_label_rect.bottom + label_padding
        self.screen.blit(self.score_image, self.score_image_rect)

        # Position high score text
        self.high_score_rect.centerx = high_score_label_rect.centerx
        self.high_score_rect.top = high_score_label_rect.bottom + label_padding
        self.screen.blit(self.high_score_image, self.high_score_rect)

        # Position level text
        self.level_rect.centerx = level_label_rect.centerx
        self.level_rect.top = level_label_rect.bottom + label_padding
        self.screen.blit(self.level_image, self.level_rect)

        # Draw ships (lives) below the lives label, centered horizontally in the header
        ship_height = self.score_image_rect.height
        total_width = (ship_height + 10) * self.stats.ships_left  # Total width of all ships including padding
        ship_x = lives_label_rect.centerx - total_width // 2
        ship_y = lives_label_rect.bottom + label_padding  # Position below the lives label

        for ship in self.ships.sprites():
            ship.rect.width = ship_height
            ship.rect.height = ship_height
            ship.rect.x = ship_x
            ship.rect.y = ship_y
            self.screen.blit(ship.image, ship.rect)
            ship_x += ship.rect.width + 10  # Space between ships

    def check_high_score(self):
        """Check to see if there's a new high score"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
