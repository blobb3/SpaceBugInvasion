import random
import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from pygame import mixer
from explosion import Explosion
import cv2
import numpy as np
from event_handler import EventHandler
from game_updates import GameUpdates
from fleet import Fleet
from game_management import GameManagement

class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()  # initializes background settings
        pygame.mixer.init()  # initializes pygame mixer for sound

        # Controlling the frame rate => function that games run at the same speed on all systems
        self.clock = pygame.time.Clock()

        # Create instances
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Space Bugged: Alien Extermination!")

        # Create an instance to store game statistics, and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # Create instance of alien ship
        self.ship = Ship(self)

        # Create Group that holds bullets and aliens
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()

        self.fleet = Fleet(self)
        self.eventhandler = EventHandler(self)
        self.gameupdates = GameUpdates(self)
        self.gamemanagement = GameManagement(self)

        self.fleet.create_fleet()

        # Start Alien Invasion in an inactive state
        self.game_active = False

        # Make the play button
        self.play_button = Button(self, "Play")

        # Load sounds
        self.start_sound = pygame.mixer.Sound('sounds/commander/mission_start.wav')
        self.start_sound.set_volume(0.5)

        self.new_mission_sound = pygame.mixer.Sound('sounds/commander/new_mission.wav')
        self.new_mission_sound.set_volume(0.5)

        self.shoot_sound = pygame.mixer.Sound('sounds/shooting/alienshoot1.wav')
        self.shoot_sound.set_volume(0.3)

        # Load and play background music
        mixer.music.load('sounds/background/MOONSTAGE_Nobass_OGG.ogg')
        mixer.music.set_volume(0.3)  # Set volume to 30%

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

            self._update_screen()  # Update the screen after checking events
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

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)  # Redraw the screen during each pass through the loop 
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for alien in self.aliens.sprites():
            alien.draw() 
        self.ship.blitme()  # Draw the ship on the screen on top of the background
        self.aliens.draw(self.screen)  # Make aliens appear
        self.explosions.draw(self.screen)  # Draw explosions

        # Draw the score information
        self.sb.show_score()

        # Draw the play button if the game is inactive
        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()  # Make the most recently drawn screen visible

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit
                self.gamemanagement.ship_hit()
                break

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
