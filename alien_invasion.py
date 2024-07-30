import random
import sys
import pygame
from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from pygame import mixer
from event_handler import EventHandler
from game_updates import GameUpdates
from fleet import Fleet
from game_management import GameManagement

class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initialize the game, and create game resources"""
        self._initialize_pygame()
        self._initialize_settings()
        self._initialize_game_elements()
        self._initialize_sounds()
        self._initialize_music()
        
    def _initialize_pygame(self):
        """Initialize pygame modules"""
        pygame.init()  # initializes background settings
        pygame.mixer.init()  # initializes pygame mixer for sound

    def _initialize_settings(self):
        """Initialize game settings"""
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Space Bugged: Alien Extermination!")
    
    def _initialize_game_elements(self):
        """Initialize game elements such as ship, bullets, aliens, etc."""
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.fleet = Fleet(self)
        self.eventhandler = EventHandler(self)
        self.gameupdates = GameUpdates(self)
        self.gamemanagement = GameManagement(self)
        self.play_button = Button(self, "Play")
        self.fleet.create_fleet()
        self.game_active = False

    def _initialize_sounds(self):
        """Load sound effects"""
        self.start_sound = pygame.mixer.Sound('sounds/commander/mission_start.wav')
        self.start_sound.set_volume(0.5)
        self.new_mission_sound = pygame.mixer.Sound('sounds/commander/new_mission.wav')
        self.new_mission_sound.set_volume(0.5)
        self.shoot_sound = pygame.mixer.Sound('sounds/shooting/alienshoot1.wav')
        self.shoot_sound.set_volume(0.3)

    def _initialize_music(self):
        """Load background music"""
        mixer.music.load('sounds/background/MOONSTAGE_Nobass_OGG.ogg')
        mixer.music.set_volume(0.3)

    # game is controlled through run_game()-method
    def run_game(self):
        """Start the main loop for the game"""
        while True:
            #create instance of the classes ship, bullets, clock
            self.eventhandler.check_events()
            dt = self.clock.tick(60) / 5000

            if self.game_active:
                self.ship.update()  # position changes, when keyboard event
                self.gameupdates.update_bullets()  # update position of bullets in while loop
                self.gameupdates.update_aliens()  # Update the position of aliens
                self.explosions.update(dt, self.settings.fleet_direction)  # Update explosion animations

            self.gameupdates.update_screen()  # Update the screen after checking events
            self.clock.tick(60)  # framerate for game -> loop runs exactly 60 times per second

    def _start_game(self):
        """Actions to start the game, including resetting stats and settings."""
        self.game_active = True
        self.stats.reset_stats()
        self.settings.initialize_dynamic_settings()
        self.sb.prep_score()
        pygame.mouse.set_visible(False)
        self.fleet.create_fleet()
        mixer.music.play(-1)  # Start or continue background music

        # Play start sound
        if self.stats.games_played == 0:
            print("Playing start sound.")
            self.start_sound.play()
        else:
            print("Playing new mission sound.")
            self.new_mission_sound.play()

        # Pause briefly to let the sound play (adjust as needed)
        pygame.time.delay(1000)  # 1000 milliseconds delay (1 second)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:

            # Play start sound
            if self.stats.games_played == 0:
                self.start_sound.play()
            else:
                self.new_mission_sound.play()

            # Pause briefly to let the sound play (adjust as needed)
            pygame.time.delay(1000)  # 1000 milliseconds delay (1 second)

            # Start background music
            mixer.music.play(-1)  # -1 plays the music in an infinite loop

            # Reset the game settings
            self.settings.initialize_dynamic_settings()

            # Reset the game statistics
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True

            # Get rid of any remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship
            self.fleet.create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor
            pygame.mouse.set_visible(False)

            # Increment games_played
            self.stats.games_played += 1

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
