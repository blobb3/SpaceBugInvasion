import sys
import pygame
from settings import Settings

class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__ (self):
        """Initialize the game, and create game resources"""
        pygame.init()  # initializes background settings

        # Controlling the frame rate => function that games run at the same speed on all systems
        self.clock = pygame.time.Clock()

        # Create instance of settings
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height)) # dimension of game window
        pygame.display.set_caption("Alien Invasion") # creates display window

        # Set the background color
        self.bg_color = (230, 230, 230)

    # game is controlled through run_game()-method
    def run_game(self):
        """Start the main loop for the game"""
        while True: 
            # Watch for keyboard and mouse events
            for event in pygame.event.get(): #returns a list of single events (any keyboard or mouse events)
                if event.tpe == pygame.QUIT:
                    sys.exit()

            # Redraw the screen during each pass through the loop
            self.screen.fill(self.settings.bg_color)
            
            # Make the most recently drawn screen visible
            pygame.display.flip()

            #create instance of the class Clock
            self.clock.tick(60) # framerate for game -> loop runs exactly 60 times per second



if __name__ == '__main__':
    # Mke a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()

