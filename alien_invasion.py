import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import  Bullet
from alien import Alien

class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()  # initializes background settings

        # Controlling the frame rate => function that games run at the same speed on all systems
        self.clock = pygame.time.Clock()

        # Create instance of settings
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Create instance of alien ship
        self.ship = Ship(self)

        # Create Group that holds bullets and aliens
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    # game is controlled through run_game()-method
    def run_game(self):
        """Start the main loop for the game"""
        while True: 
            #create instance of the classes ship, bullets, clock
            self._check_events()
            self.ship.update() # position changes, when keyboard event
            self.bullets.update() # update position of bullets in while loop
            self._update_aliens() # Update the position of aliens
            self._update_screen()  # Update the screen after checking events
            self.clock.tick(60) # framerate for game -> loop runs exactly 60 times per second

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()            

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien width and one alien height.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x = alien_width
        current_y = alien_height  # Fixed y position for a single row
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width  # Move to the next position horizontally

            # Finished a row; reset x value, and increment y value
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the fleet."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color) # Redraw the screen during each pass through the loop 
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme() # Draw the ship on the screen on top of the background
        self.aliens.draw(self.screen) # make aliens appear

        pygame.display.flip() # Make the most recently drawn screen visible

    def _update_aliens(self):
        """Update the positions of all aliens in the fleet"""
        self.aliens.update()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
