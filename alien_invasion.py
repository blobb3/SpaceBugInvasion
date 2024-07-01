import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import  Bullet

class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()  # initializes background settings

        # Controlling the frame rate => function that games run at the same speed on all systems
        self.clock = pygame.time.Clock()

        # Create instance of settings
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN) #figures out a window size that will fill the screen
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion Game") # creates display window

        # Create instance of alien ship
        self.ship = Ship(self)

        # Create Group that holds bullet
        self.bullets = pygame.sprite.Group() 

        # Set the background color
        self.bg_color = (15, 15, 70) 

    # game is controlled through run_game()-method
    def run_game(self):
        """Start the main loop for the game"""
        while True: 
            self._check_events()
            self.ship.update() # position changes, when keyboard event
            self.bullets.update() # update position of bullets in while loop
            self._update_screen()  # Update the screen after checking events

            #create instance of the class Clock
            self.clock.tick(60) # framerate for game -> loop runs exactly 60 times per second

    def _check_events(self):
        """Respond to keypresses and mouse events""" 
        for event in pygame.event.get(): #returns a list of single events (any keyboard or mouse events)
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN: # when key pressed
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                        
    def _check_keydown_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right =False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)
        
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        self.screen.fill(self.bg_color)  # Redraw the screen during each pass through the loop 
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()  # Draw the ship on the screen on top of the background
        pygame.display.flip()  # Make the most recently drawn screen visible

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
