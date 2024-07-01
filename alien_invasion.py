import sys
import pygame
from settings import Settings
from ship import Ship

class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()  # initializes background settings

        # Controlling the frame rate => function that games run at the same speed on all systems
        self.clock = pygame.time.Clock()

        # Create instance of settings
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height)) # dimension of game window
        pygame.display.set_caption("Alien Invasion") # creates display window

        # Create instance of alien ship
        self.ship = Ship(self)

        # Set the background color
        self.bg_color = (15, 15, 70)  # dark blue

    # game is controlled through run_game()-method
    def run_game(self):
        """Start the main loop for the game"""
        while True: 
            self._check_events()
            self._update_screen()  # Update the screen after checking events

            #create instance of the class Clock
            self.clock.tick(60) # framerate for game -> loop runs exactly 60 times per second

    def _check_events(self):
        """Respond to keypresses and mouse events""" 
        for event in pygame.event.get(): #returns a list of single events (any keyboard or mouse events)
                if event.type == pygame.QUIT:
                    sys.exit()
        
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        self.screen.fill(self.bg_color)  # Redraw the screen during each pass through the loop 
        self.ship.blitme()  # Draw the ship on the screen on top of the background
        pygame.display.flip()  # Make the most recently drawn screen visible

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
