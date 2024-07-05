import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import  Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from pygame import mixer
import cv2
import numpy as np

class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()  # initializes background settings
        pygame.mixer.init()  # initializes pygame mixer for sound

        # Controlling the frame rate => function that games run at the same speed on all systems
        self.clock = pygame.time.Clock()

        # Create instance of settings
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

        self._create_fleet()

        # Start Alien Invasion in an inactive state
        self.game_active = False

        # Make the play button
        self.play_button = Button(self, "Play")

         # Load sounds
        self.start_sound = pygame.mixer.Sound('sounds/commander/mission_start.wav')
        self.start_sound.set_volume(0.5)

        # Load and play background music
        mixer.music.load('sounds/background/MOONSTAGE_Nobass_OGG.ogg')
        mixer.music.set_volume(0.3)  # Set volume to 30%

    # game is controlled through run_game()-method
    def run_game(self):
        """Start the main loop for the game"""
        while True: 
            #create instance of the classes ship, bullets, clock
            self._check_events()

            if self.game_active: 
                self.ship.update() # position changes, when keyboard event
                self._update_bullets() # update position of bullets in while loop
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
            # start the game when the player clicks play
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

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
        self._check_bullet_alien_collisions()
    
    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions"""
        #Remove any bullets and aliens that have collided
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )
        if collisions:
            for aliens in collisions.values():
                for alien in aliens:
                    self._play_explosion(alien.rect.center)  # Play explosion at the alien's position
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            #Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()

            # Increase Level
            self.stats.level += 1
            self.sb.prep_level()

    def _play_explosion(self, position):
        """Play explosion video at the given position"""
        explosion = cv2.VideoCapture('images/explosion.avi')
        
        while explosion.isOpened():
            ret, frame = explosion.read()
            if not ret:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (64, 64))  # Resize to fit in the game
            
            # Convert frame to pygame surface
            frame_surface = pygame.surfarray.make_surface(frame)
            
            # Get the rectangle for positioning
            rect = frame_surface.get_rect(center=position)
            
            # Blit the frame onto the screen
            self.screen.blit(frame_surface, rect)
            pygame.display.flip()
            
            # Control the frame rate of the video
            self.clock.tick(30)

        explosion.release()

    def _create_fleet(self):
        """Create the fleet of aliens."""
        alien_images = ['images/alien1.png', 'images/alien2.png', 'images/alien3.png']
        # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien width and one alien height.
        alien = Alien(self, alien_images[0])
        alien_width, alien_height = alien.rect.size

        current_x = alien_width
        current_y = alien_height  # Fixed y position for a single row
        row_index = 0
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - alien_width):
                image_path = alien_images[row_index % len(alien_images)]
                self._create_alien(current_x, current_y, image_path)
                current_x += 2 * alien_width  # Move to the next position horizontally

            # Finished a row; reset x value, and increment y value
            current_x = alien_width
            current_y += 2 * alien_height
            row_index += 1

    def _create_alien(self, x_position, y_position, image_path):
        """Create an alien and place it in the fleet."""
        new_alien = Alien(self, image_path)
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

        # Draw the score information
        self.sb.show_score()

        # Draw the play button if the game is inactive
        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip() # Make the most recently drawn screen visible

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update positions"""
        self._check_fleet_edges()
        self.aliens.update()

        # look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("Bug Alert! Ship infested!")

        # look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()
    
    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleets direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left, and update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            #Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #Pause
            sleep(0.5) #pauses program execution for half a second
        else:
            self.game_active = False # when the player has no ships left => game active is false
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                #Treat this the same as if the ship got hit
                self._ship_hit()
                break
    
    def _check_play_button(self, mouse_pos):
        """Start a new game when the palyer clicks play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:

            # Play start sound
            self.start_sound.play()

            # Pause briefly to let the sound play (adjust as needed)
            pygame.time.delay(500)  # 500 milliseconds delay (0.5 seconds)

            # Start background music
            mixer.music.play(-1)  # -1 plays the music in an infinite loop

            # reset the game settings
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
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor
            pygame.mouse.set_visible(False)

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
