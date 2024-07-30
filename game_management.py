import pygame
from time import sleep
from explosion import Explosion

class GameManagement:
    def __init__(self, ai_game):
        """Initialize the game management attributes."""
        self.ai_game = ai_game

    def ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.ai_game.stats.ships_left > 0:
            # Decrement ships_left, and update scoreboard
            self.ai_game.stats.ships_left -= 1
            self.ai_game.sb.prep_ships()

            # Get rid of any remaining bullets and aliens
            self.ai_game.bullets.empty()
            self.ai_game.aliens.empty()

            # Create a new fleet and center the ship
            self.ai_game.fleet.create_fleet()
            self.ai_game.ship.center_ship()

            # Pause
            sleep(0.5)  # pauses program execution for half a second
        else:
            self.ai_game.game_active = False  # when the player has no ships left => game active is false
            pygame.mouse.set_visible(True)

    def check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        collisions = pygame.sprite.groupcollide(self.ai_game.bullets, self.ai_game.aliens, True, False)

        # Process collisions
        for bullet in collisions:
            for alien in collisions[bullet]:
                # Call take_hit, which decrements an alien's life or destroys it
                if alien.take_hit():
                    # Create an explosion effect at the alien's center
                    explosion = Explosion(self.ai_game, alien.rect.center)
                    self.ai_game.explosions.add(explosion)
                    # Remove the alien from the group
                    self.ai_game.aliens.remove(alien)
                    # Update the score
                    self.ai_game.stats.score += self.ai_game.settings.alien_points
                    self.ai_game.sb.prep_score()
                    self.ai_game.sb.check_high_score()

        # If all aliens are destroyed, reset the level
        if not self.ai_game.aliens:
            self.start_new_level()

    def start_new_level(self):
        """Handles the logic to start a new level."""
        # Destroy existing bullets, reset bullet group
        self.ai_game.bullets.empty()
        # Create a new fleet of aliens
        self.ai_game.fleet.create_fleet()
        # Increase the level count
        self.ai_game.stats.level += 1
        self.ai_game.sb.prep_level()
        # Possibly increase game difficulty here
        self.ai_game.settings.increase_speed()
